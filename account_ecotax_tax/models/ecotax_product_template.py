# Copyright 2024 Akretion (https://www.akretion.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    country_fixed_ecotax = fields.Float(
        compute="_compute_country_fixed_ecotax",
        help="Country-specific fixed ecotax, set via context at tax computation.",
    )

    def _compute_country_fixed_ecotax(self):
        for rec in self:
            rec.country_fixed_ecotax = self.env.context.get(
                "country_fixed_ecotax", rec.fixed_ecotax
            )
