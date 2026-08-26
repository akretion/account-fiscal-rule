To use this module, you need to:

1. Go to *Accounting > Configuration > Ecotax Classification*.
2. Open an existing classification or create a new one.
3. In the **Country-specific Amounts** field, enter per-country amounts
   as a JSON dictionary, e.g. `{"FR": 0.94, "IT": 0.50, "ES": 0.80}`.
4. The ecotax tax will automatically use the country-specific amount for
   partners located in that country.

If no country entry exists for a partner's country, the system falls back
to the classification's default fixed ecotax amount.
