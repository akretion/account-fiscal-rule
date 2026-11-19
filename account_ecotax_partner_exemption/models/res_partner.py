# © 2026 Akretion (http://www.akretion.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    ecotax_exempt = fields.Boolean(
        string="Ecotax exempt",
        tracking=True,
        help="Do not apply the ecotax on the documents of this customer.",
    )

    def _is_ecotax_exempt(self):
        """Tell if the ecotax must be left out of the documents of this partner.

        The flag is read on the commercial entity, so that setting it on a
        company is enough for all its contacts.
        """
        self.ensure_one()
        return self.commercial_partner_id.ecotax_exempt
