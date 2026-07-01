# Copyright 2024 Akretion (https://www.akretion.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class AccountEcotaxClassification(models.Model):
    _inherit = "account.ecotax.classification"

    country_amounts = fields.Json(
        default=dict,
        help="Per-country fixed ecotax amounts, e.g. "
        '{"FR": 0.94, "IT": 0.50, "ES": 0.80}. '
        "If no entry for a country, the default_fixed_ecotax is used.",
    )
