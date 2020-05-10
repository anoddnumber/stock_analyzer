

class CashFlowStatement:

    DATE='date'
    OPERATING_CASH_FLOW='operating_cash_flow'
    CAPITAL_EXPENDITURE='capital_expenditure'
    INVESTING_CASH_FLOW='investing_cash_flow'
    DEBT_REPAYMENT='debt_repayment'
    SHARE_BUYBACK='share_buyback'
    DIVIDEND_PAYMENTS='dividend_payments'
    FINANCING_CASH_FLOW='financing_cash_flow'
    NET_CASH_FLOW='net_cash_flow'
    FREE_CASH_FLOW='free_cash_flow'

    available_attributes = frozenset({DATE, OPERATING_CASH_FLOW, CAPITAL_EXPENDITURE,
                                      INVESTING_CASH_FLOW, DEBT_REPAYMENT, SHARE_BUYBACK,
                                      DIVIDEND_PAYMENTS, FINANCING_CASH_FLOW, NET_CASH_FLOW,
                                      FREE_CASH_FLOW})

    def __init__(self, mapping, json_data):
        if mapping is not None and json_data is not None:
            for key in mapping:
                if key not in self.available_attributes:
                    print('Key ' + str(key) + ' is not allowed in an Cash Flow Statement')
                    continue
                json_data_key = mapping[key]
                try:
                    setattr(self, key, json_data[json_data_key])
                except KeyError:
                    print('Cash Flow Statement: JSON key ' + str(json_data_key) + ' not found in json_data' + str(json_data))

    def __str__(self):
        res = ''
        for attribute in sorted(self.available_attributes):
            res += attribute + ' : ' + getattr(self, attribute, 'missing') + '\n'
        return res
