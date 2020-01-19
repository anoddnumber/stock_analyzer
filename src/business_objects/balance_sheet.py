

class BalanceSheet:
    DATE = 'date'
    CASH_AND_CASH_EQUIVALENTS = 'cash_and_cash_equivalents'
    ACCOUNTS_RECEIVABLE = 'accounts_receivable'
    INVENTORY = 'inventory'
    CURRENT_ASSETS = 'current_assets'
    FIXED_ASSETS = 'fixed_assets'
    INTANGIBLE_ASSETS = 'intangible_assets'
    NON_CURRENT_ASSETS = 'non_current_assets'
    TOTAL_ASSETS = 'total_assets'
    ACCOUNTS_PAYABLE = 'accounts_payable'
    CURRENT_LIABILITIES = 'current_liabilities'
    TOTAL_DEBT = 'total_debt'
    NON_CURRENT_LIABILITIES = 'non_current_liabilities'
    TOTAL_LIABILITIES = 'total_liabilities'
    RETAINED_EARNINGS = 'retained_earnings'
    SHAREHOLDERS_EQUITY = 'shareholders_equity'

    available_attributes = frozenset({DATE, CASH_AND_CASH_EQUIVALENTS, ACCOUNTS_RECEIVABLE,
                                      INVENTORY, CURRENT_ASSETS, FIXED_ASSETS,
                                      INTANGIBLE_ASSETS, NON_CURRENT_ASSETS, TOTAL_ASSETS,
                                      ACCOUNTS_PAYABLE, CURRENT_LIABILITIES, TOTAL_DEBT,
                                      NON_CURRENT_LIABILITIES, TOTAL_LIABILITIES, RETAINED_EARNINGS,
                                      SHAREHOLDERS_EQUITY})

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
