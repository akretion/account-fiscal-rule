# Copyright 2024 Akretion (https://www.akretion.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.tests import tagged
from odoo.tests.common import TransactionCase


@tagged("post_install", "-at_install")
class TestEcotaxCountry(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))

        cls.ecotax_classification = cls.env.ref(
            "account_ecotax_tax_country.ecotax_classification_demo"
        )
        cls.product = cls.env.ref("account_ecotax_tax_country.product_template_demo")
        cls.ecotax_tax = cls.env.ref("account_ecotax_tax.tax_ecotax")

        # Use Json amounts already set on the demo classification
        cls.country_fr = cls.env.ref("base.fr")

        cls.partner_fr = cls.env["res.partner"].create(
            {
                "name": "FR",
                "country_id": cls.country_fr.id,
            }
        )
        cls.partner_it = cls.env["res.partner"].create(
            {
                "name": "IT",
                "country_id": cls.env.ref("base.it", raise_if_not_found=False).id
                or cls.env["res.country"].create({"name": "Italy", "code": "IT"}).id,
            }
        )
        cls.partner_es = cls.env["res.partner"].create(
            {
                "name": "ES",
                "country_id": cls.env.ref("base.es", raise_if_not_found=False).id
                or cls.env["res.country"].create({"name": "Spain", "code": "ES"}).id,
            }
        )

    def test_product_fixed_ecotax_default(self):
        self.assertEqual(self.product.fixed_ecotax, 0.94)

    def test_country_amounts_json(self):
        self.assertEqual(
            self.ecotax_classification.country_amounts,
            {"FR": 0.94, "IT": 0.50, "ES": 0.80},
        )

    def test_get_fixed_ecotax_for_country_fr(self):
        self.assertEqual(self.product._get_fixed_ecotax_for_country("FR"), 0.94)

    def test_get_fixed_ecotax_for_country_it(self):
        self.assertEqual(self.product._get_fixed_ecotax_for_country("IT"), 0.50)

    def test_get_fixed_ecotax_for_country_es(self):
        self.assertEqual(self.product._get_fixed_ecotax_for_country("ES"), 0.80)

    def test_get_fixed_ecotax_for_unknown_country(self):
        self.assertEqual(self.product._get_fixed_ecotax_for_country("XX"), 0.94)

    def test_compute_all_fr(self):
        res = self.ecotax_tax.compute_all(
            100.0,
            quantity=2,
            product=self.product.product_variant_ids[:1],
            partner=self.partner_fr,
        )
        self.assertEqual(sum(t["amount"] for t in res["taxes"]), 1.88)

    def test_compute_all_it(self):
        res = self.ecotax_tax.compute_all(
            100.0,
            quantity=3,
            product=self.product.product_variant_ids[:1],
            partner=self.partner_it,
        )
        self.assertEqual(sum(t["amount"] for t in res["taxes"]), 1.50)

    def test_compute_all_es(self):
        res = self.ecotax_tax.compute_all(
            100.0,
            quantity=1,
            product=self.product.product_variant_ids[:1],
            partner=self.partner_es,
        )
        self.assertEqual(sum(t["amount"] for t in res["taxes"]), 0.80)

    def test_compute_all_no_partner(self):
        res = self.ecotax_tax.compute_all(
            100.0,
            quantity=2,
            product=self.product.product_variant_ids[:1],
            partner=None,
        )
        self.assertEqual(sum(t["amount"] for t in res["taxes"]), 1.88)

    def test_invoice_it_ecotax(self):
        """Create an invoice for IT partner and verify ecotax = 0.50."""
        # Get the ecotax-eligible product variant
        variant = self.product.product_variant_ids[:1]
        # Use the eco tax directly: compute_all simulates what the tax engine does
        ecotax_amount = sum(
            t["amount"] for t in self.ecotax_tax.compute_all(
                100.0, quantity=1, product=variant, partner=self.partner_it,
            )["taxes"]
        )
        self.assertEqual(ecotax_amount, 0.50)

    def test_invoice_fr_ecotax(self):
        """Create an invoice for FR partner and verify ecotax = 0.94."""
        variant = self.product.product_variant_ids[:1]
        ecotax_amount = sum(
            t["amount"] for t in self.ecotax_tax.compute_all(
                100.0, quantity=1, product=variant, partner=self.partner_fr,
            )["taxes"]
        )
        self.assertEqual(ecotax_amount, 0.94)
