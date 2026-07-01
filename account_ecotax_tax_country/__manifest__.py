{
    "name": "Ecotax Tax Multi-Country",
    "summary": "Extends account_ecotax_tax with per-country fixed ecotax amounts",
    "version": "18.0.1.0.0",
    "author": "Akretion, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/account-fiscal-rule",
    "category": "Localization/Account Taxes",
    "license": "AGPL-3",
    "depends": [
        "account_ecotax_tax",
    ],
    "data": [
        "views/account_ecotax_classification_view.xml",
    ],
    "demo": [
        "data/ecotax_country_demo.xml",
    ],
    "installable": True,
}
