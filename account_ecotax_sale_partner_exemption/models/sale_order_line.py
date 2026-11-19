# © 2026 Akretion (http://www.akretion.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def _get_ecotax_eligible_classification(self):
        """No ecotax on the sale orders of an exempt customer.

        The ecotax lines and the ecotax taxes of the sale order lines are both
        generated from this method (see account_ecotax_sale_tax).
        """
        self.ensure_one()
        partner = self.order_id.partner_id
        if partner and partner._is_ecotax_exempt():
            return self.env["ecotax.line.product"]
        return super()._get_ecotax_eligible_classification()
