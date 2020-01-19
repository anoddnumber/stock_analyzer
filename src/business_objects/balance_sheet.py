

class BalanceSheet:

    available_attributes = frozenset({'date', 'cash_and_cash_equivalents', 'accounts_receivable'
                                      'inventory', 'current_assets', 'fixed_assets',
                                      'intangible_assets', 'non_current_assets', 'total_assets',
                                      'accounts_payable', 'current_liabilities', 'total_debt',
                                      'non_current_liabilities', 'total_liabilities', 'retained_earnings',
                                      'shareholders_equity'})

    def __init__(self, mapping, json_data):
        if mapping is not None and json_data is not None:
            for key in mapping:
                if key not in self.available_attributes:
                    print('Key ' + str(key) + ' is not allowed in a Balance Sheet')
                    continue
                json_data_key = mapping[key]
                try:
                    self[key] = json_data[json_data_key]
                except KeyError:
                    print('Balance Sheet: JSON key ' + str(json_data_key) + ' not found in json_data' + str(json_data))
