# Copyright 2024 Akretion (https://www.akretion.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class AccountTax(models.Model):
    _inherit = "account.tax"

    @api.model
    def compute_all(
        self,
        price_unit,
        currency=None,
        quantity=1.0,
        product=None,
        partner=None,
        **kwargs,
    ):
        """Inject country-specific ecotax by overriding fixed_ecotax on the product."""
        backup = None
        tmpl = None
        if product and partner and partner.country_id:
            tmpl = getattr(product, "product_tmpl_id", product)
            country_amount = tmpl._get_fixed_ecotax_for_country(
                partner.country_id.code,
            )
            if country_amount != tmpl.fixed_ecotax:
                backup = tmpl.fixed_ecotax
                # Bypass computed field inverse: write directly to DB
                self.env.cr.execute(
                    "UPDATE product_template SET fixed_ecotax = %s WHERE id = %s",
                    (country_amount, tmpl.id),
                )
                tmpl.invalidate_recordset(["fixed_ecotax"])
        try:
            return super().compute_all(
                price_unit,
                currency=currency,
                quantity=quantity,
                product=product,
                partner=partner,
                **kwargs,
            )
        finally:
            if backup is not None and tmpl:
                self.env.cr.execute(
                    "UPDATE product_template SET fixed_ecotax = %s WHERE id = %s",
                    (backup, tmpl.id),
                )
                tmpl.invalidate_recordset(["fixed_ecotax"])


class ProductTemplate(models.Model):
    _inherit = "product.template"

    def _get_fixed_ecotax_for_country(self, country_code):
        """Look up per-country amount from classification Json field."""
        self.ensure_one()
        if not country_code:
            return self.fixed_ecotax
        classification = self._get_ecotax_classification()
        if (
            classification
            and classification.country_amounts
            and country_code in classification.country_amounts
        ):
            return classification.country_amounts[country_code]
        return self.fixed_ecotax

    def _get_ecotax_classification(self):
        """Get the active ecotax classification for this product."""
        self.ensure_one()
        for line in self.ecotax_line_product_ids:
            if line.classification_id.active:
                return line.classification_id
        return self.env["account.ecotax.classification"]
