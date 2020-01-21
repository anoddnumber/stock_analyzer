

class CompanyReport:

    TICKER = 'ticker'

    # Big 5
    RETURN_ON_INVESTED_CAPITAL = 'return_on_invested_capital'
    REVENUE_GROWTH = 'revenue_growth'
    EARNINGS_GROWTH = 'earnings_growth'
    EQUITY_GROWTH = 'equity_growth'
    CASH_GROWTH = 'cash_growth'

    # Other considerations
    HISTORIC_PE = 'historic_pe'
    TOTAL_DEBT = 'total_debt'
    MARGIN_OF_SAFETY = 'margin_of_safety'

    available_attributes = frozenset({TICKER, RETURN_ON_INVESTED_CAPITAL, REVENUE_GROWTH,
                                      EARNINGS_GROWTH, EQUITY_GROWTH, CASH_GROWTH,
                                      HISTORIC_PE, TOTAL_DEBT, MARGIN_OF_SAFETY})

    def __init__(self):
        pass

    def set_attr(self, attr, value):
        if attr not in self.available_attributes:
            raise AttributeError('Cannot set attribute ' + str(attr) + ' to CompanyReport, it is not a supported attribute')
        self[attr] = value;