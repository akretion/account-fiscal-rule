This module extends `account_ecotax_tax` with per-country fixed ecotax amounts.

It adds a `country_amounts` Json field on the ecotax classification where
you can define different ecotax amounts per country (e.g., France, Italy,
Spain). The correct country amount is automatically selected based on the
partner's country at tax computation time.

When this module is not installed, the ecotax system continues to work as
before, using the default `fixed_ecotax` from the product.
