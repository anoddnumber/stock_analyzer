

class CompanyReport:

    TICKER = 'ticker'

    # Big 5 - should be greater than or equal to 10% per year for the last 10 years for each of them
    # These are in order of importance
    # Check the 5 year and 1 year marks to make sure it isn't slowing down

    # ROIC is the rate of return a business makes from the money it invests into itself
    # calculated as net operating profit after tax / (equity + debt)
    # net operating profit after tax (NOPAT) = net income + interest expenses + depreciation expenses
    # according to investopedia, NOPAT = net income - dividends
    # NOPAT = operating income - tax expense (?)
    RETURN_ON_INVESTED_CAPITAL_10_YEAR = 'return_on_invested_capital_10_year'
    RETURN_ON_INVESTED_CAPITAL_5_YEAR = 'return_on_invested_capital_5_year'
    RETURN_ON_INVESTED_CAPITAL_1_YEAR = 'return_on_invested_capital_1_year'

    EQUITY_GROWTH = 'equity_growth'
    EARNINGS_GROWTH = 'earnings_growth'
    REVENUE_GROWTH = 'revenue_growth'
    CASH_GROWTH = 'cash_growth'

    # Other considerations
    HISTORIC_PE = 'historic_pe'
    TOTAL_DEBT = 'total_debt'
    MARGIN_OF_SAFETY = 'margin_of_safety'

    available_attributes = frozenset({TICKER,
                                      RETURN_ON_INVESTED_CAPITAL_10_YEAR, RETURN_ON_INVESTED_CAPITAL_5_YEAR,
                                      RETURN_ON_INVESTED_CAPITAL_1_YEAR,
                                      EQUITY_GROWTH,
                                      EARNINGS_GROWTH,
                                      REVENUE_GROWTH,
                                      CASH_GROWTH,
                                      HISTORIC_PE, TOTAL_DEBT, MARGIN_OF_SAFETY})

    def __init__(self):
        pass

    def set_attr(self, attr, value):
        if attr not in self.available_attributes:
            raise AttributeError('Cannot set attribute ' + str(attr) + ' to CompanyReport, it is not a supported attribute')
        setattr(self, attr, value)

    def __str__(self):
        res = ''
        for attribute in sorted(self.available_attributes):
            res += attribute + ' : ' + str(getattr(self, attribute, 'missing')) + '\n'
        return res
