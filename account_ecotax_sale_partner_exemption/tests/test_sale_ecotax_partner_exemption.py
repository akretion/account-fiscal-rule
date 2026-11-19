# © 2026 Akretion (http://www.akretion.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import Command

from odoo.addons.base.tests.common import BaseCommon


class TestSaleEcotaxExemption(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        cls.classification = cls.env["account.ecotax.classification"].create(
            {
                "name": "Fixed Ecotax",
                "ecotax_type": "fixed",
                "default_fixed_ecotax": 5.0,
                "product_status": "M",
                "supplier_status": "IMP",
            }
        )
        cls.product = cls.env["product.product"].create(
            {
                "name": "Ecotax product",
                "list_price": 100.0,
                "ecotax_line_product_ids": [
                    Command.create({"classification_id": cls.classification.id})
                ],
            }
        )
        cls.customer = cls.env["res.partner"].create({"name": "Customer"})
        cls.exempt_customer = cls.env["res.partner"].create(
            {"name": "Exempt customer", "ecotax_exempt": True}
        )

    def _make_order(self, partner):
        return self.env["sale.order"].create(
            {
                "partner_id": partner.id,
                "order_line": [
                    Command.create({"product_id": self.product.id, "price_unit": 100.0})
                ],
            }
        )

    def test_ecotax_on_customer(self):
        order = self._make_order(self.customer)
        self.assertEqual(order.order_line.ecotax_line_ids.amount_total, 5.0)
        self.assertEqual(order.amount_ecotax, 5.0)

    def test_no_ecotax_on_exempt_customer(self):
        order = self._make_order(self.exempt_customer)
        self.assertFalse(order.order_line.ecotax_line_ids)
        self.assertEqual(order.amount_ecotax, 0.0)
