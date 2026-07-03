# Copyright 2024 Akretion (https://www.akretion.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    country_fixed_ecotax = fields.Float(
        string="Country Fixed Ecotax",
        default=0.0,
        help="Country-specific fixed ecotax, set at tax computation time.",
    )
