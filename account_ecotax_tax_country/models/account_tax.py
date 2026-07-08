# Copyright 2024 Akretion (https://www.akretion.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class AccountTax(models.Model):
    _inherit = "account.tax"

    @api.model
    def _eval_taxes_computation_prepare_product_values(
        self, default_product_values, product=None
    ):
        """Inject country-specific ecotax into product values dict.

        The ecotax tax formula reads ``product['fixed_ecotax']`` (or
        ``product['country_fixed_ecotax']``), so we override both keys
        from the ``country_fixed_ecotax`` context key set by
        :meth:`compute_all`.
        """
        product_values = super()._eval_taxes_computation_prepare_product_values(
            default_product_values, product=product
        )
        country_amount = self.env.context.get("country_fixed_ecotax")
        if country_amount is not None:
            product_values["fixed_ecotax"] = country_amount
            product_values["country_fixed_ecotax"] = country_amount
        return product_values

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
        """Pass the country-specific ecotax amount through context.

        ``compute_all`` is the public entry point for tax computation.
        We detect the partner's country, look up the matching amount on
        the product's ecotax classification, and pass it via context so
        that :meth:`_eval_taxes_computation_prepare_product_values` can
        inject it into the product-values dict used by the formula —
        without mutating the database.
        """
        if product and partner and partner.country_id:
            tmpl = getattr(product, "product_tmpl_id", product)
            country_amount = tmpl._get_fixed_ecotax_for_country(
                partner.country_id.code,
            )
            if country_amount != tmpl.fixed_ecotax:
                return super(
                    AccountTax, self.with_context(country_fixed_ecotax=country_amount)
                ).compute_all(
                    price_unit,
                    currency=currency,
                    quantity=quantity,
                    product=product,
                    partner=partner,
                    **kwargs,
                )
        return super().compute_all(
            price_unit,
            currency=currency,
            quantity=quantity,
            product=product,
            partner=partner,
            **kwargs,
        )


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
