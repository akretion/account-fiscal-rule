# © 2014-2024 Akretion (http://www.akretion.com)
#   @author Mourad EL HADJ MIMOUNE <mourad.elhadj.mimoune@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class AccountTax(models.Model):
    _inherit = "account.tax"

    is_ecotax = fields.Boolean(
        "Ecotax",
        help="Warning : To include Ecotax "
        "in the VAT tax check this :\n"
        '1: check  "included in base amount "\n'
        "2: The Ecotax sequence must be less then "
        "VAT tax (in sale and purchase)",
    )

    @api.onchange("is_ecotax")
    def onchange_is_ecotax(self):
        if self.is_ecotax:
            self.amount_type = "code"
            self.include_base_amount = True
            self.formula = "quantity and product.country_fixed_ecotax * quantity or 0.0"

    def _eval_taxes_computation_prepare_product_fields(self):
        return super()._eval_taxes_computation_prepare_product_fields() | {
            "fixed_ecotax",
            "weight_based_ecotax",
            "ecotax_amount",
            "weight",
            "country_fixed_ecotax",
        }

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
        """Pass through (actual country logic in account_ecotax_tax_country)."""
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

    country_fixed_ecotax = fields.Float(
        default=0.0,
        help="Country-specific fixed ecotax, set at tax computation time.",
    )
