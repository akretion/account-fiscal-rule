# © 2026 Akretion (http://www.akretion.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    def _get_ecotax_eligible_classification(self):
        """No ecotax on the documents of an exempt customer.

        Overriding the single eligibility entry point is enough: the ecotax
        lines are generated from it and the ecotax taxes are selected from it
        (see account_ecotax_tax), whatever the installed modules.
        """
        self.ensure_one()
        partner = self.move_id.partner_id
        if partner and partner._is_ecotax_exempt():
            return self.env["ecotax.line.product"]
        return super()._get_ecotax_eligible_classification()
