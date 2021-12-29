import locale

# Formatting budget in user table
def prettier_budget(self, with_prefix=True, decimal=0):
    locale.setlocale(locale.LC_NUMERIC, 'IND')
    rupiah = locale.format_string("%.*f", (decimal, self.budget), True)
    if with_prefix:
        return "Rp. {}".format(rupiah)
    return rupiah

# Formatting price in item table
def prettier_price(self, with_prefix=True, decimal=0):
    locale.setlocale(locale.LC_NUMERIC, 'IND')
    rupiah = locale.format_string("%.*f", (decimal, self.price), True)
    if with_prefix:
        return "Rp. {}".format(rupiah)
    return rupiah
