

class IncomeStatement:

    available_attributes = frozenset({'date', 'revenue', 'cost_of_revenue',
                                      'gross_profit', 'r_and_d_expenses', 's_g_and_a_expenses',
                                      'operating_expenses', 'interest_expenses', 'earnings_before_tax',
                                      'income_tax_expense', 'net_income', 'eps', 'eps_diluted'})

    def __init__(self, mapping, json_data):
        if mapping is not None and json_data is not None:
            for key in mapping:
                if key not in self.available_attributes:
                    print('Key ' + str(key) + ' is not allowed in an Income Statement')
                    continue
                json_data_key = mapping[key]
                try:
                    self[key] = json_data[json_data_key]
                except KeyError:
                    print('Income Statement: JSON key ' + str(json_data_key) + ' not found in json_data' + str(json_data))
