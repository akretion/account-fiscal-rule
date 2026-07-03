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
        """Inject country-specific ecotax by adjusting result."""
        result = super().compute_all(
            price_unit,
            currency=currency,
            quantity=quantity,
            product=product,
            partner=partner,
            **kwargs,
        )
        # Override ecotax amounts when partner country has a specific rate
        if product and partner and partner.country_id:
            tmpl = getattr(product, "product_tmpl_id", product)
            amount = tmpl._get_fixed_ecotax_for_country(
                partner.country_id.code,
            )
            # Only adjust if different from default (which the formula already computed)
            if amount != tmpl.fixed_ecotax:
                for tax_dict in result["taxes"]:
                    tax_dict["amount"] = amount * quantity
        return result


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
