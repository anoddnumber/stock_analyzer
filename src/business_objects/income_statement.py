

class IncomeStatement:
    TICKER = 'ticker'
    DATE = 'date'
    REVENUE = 'revenue'
    COST_OF_REVENUE = 'cost_of_revenue'
    GROSS_PROFIT = 'gross_profit'
    R_AND_D_EXPENSES = 'r_and_d_expenses'
    S_G_AND_A_EXPENSES = 's_g_and_a_expenses'
    OPERATING_EXPENSES = 'operating_expenses'
    INTEREST_EXPENSES = 'interest_expenses'
    EARNINGS_BEFORE_TAX = 'earnings_before_tax'
    INCOME_TAX_EXPENSE = 'income_tax_expense'
    NET_INCOME = 'net_income'
    EPS = 'eps'
    EPS_DILUTED = 'eps_diluted'

    available_attributes = frozenset({TICKER, DATE, REVENUE, COST_OF_REVENUE,
                                      GROSS_PROFIT, R_AND_D_EXPENSES, S_G_AND_A_EXPENSES,
                                      OPERATING_EXPENSES, INTEREST_EXPENSES, EARNINGS_BEFORE_TAX,
                                      INCOME_TAX_EXPENSE, NET_INCOME, EPS, EPS_DILUTED})

    def __init__(self, ticker, mapping, json_data):
        setattr(self, 'ticker', ticker)

        if mapping is not None and json_data is not None:
            for key in mapping:
                if key not in self.available_attributes:
                    print('Key ' + str(key) + ' is not allowed in an Income Statement')
                    continue
                json_data_key = mapping[key]
                try:
                    # print('key: ' + str(key))
                    # print('json_data_key: ' + json_data_key)
                    setattr(self, key, json_data[json_data_key])
                    # self['abc'] = 'abc'
                    # self[key] = json_data[json_data_key]
                except KeyError:
                    print('Income Statement: JSON key ' + str(json_data_key) + ' not found in json_data' + str(json_data))

    def __str__(self):
        res = ''
        for attribute in sorted(self.available_attributes):
            res += attribute + ' : ' + getattr(self, attribute, 'missing') + '\n'
        return res
