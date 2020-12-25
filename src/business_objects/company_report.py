

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

    EQUITY_GROWTH_10_YEAR = 'equity_growth_10_year'
    EQUITY_GROWTH_5_YEAR = 'equity_growth_5_year'
    EQUITY_GROWTH_3_YEAR = 'equity_growth_1_year'
    EQUITY_GROWTH_1_YEAR = 'equity_growth_1_year'

    EARNINGS_GROWTH_10_YEAR = 'earnings_growth_10_year'
    EARNINGS_GROWTH_5_YEAR = 'earnings_growth_5_year'
    EARNINGS_GROWTH_3_YEAR = 'earnings_growth_3_year'
    EARNINGS_GROWTH_1_YEAR = 'earnings_growth_1_year'

    REVENUE_GROWTH_10_YEAR = 'revenue_growth_10_year'
    REVENUE_GROWTH_5_YEAR = 'revenue_growth_5_year'
    REVENUE_GROWTH_3_YEAR = 'revenue_growth_3_year'
    REVENUE_GROWTH_1_YEAR = 'revenue_growth_1_year'

    OPERATING_CASH_GROWTH_10_YEAR = 'cash_growth_10_year'
    OPERATING_CASH_GROWTH_5_YEAR = 'cash_growth_5_year'
    OPERATING_CASH_GROWTH_3_YEAR = 'cash_growth_3_year'
    OPERATING_CASH_GROWTH_1_YEAR = 'cash_growth_1_year'

    TOTAL_DEBT_10_YEAR = 'total_debt_10_year'
    TOTAL_DEBT_5_YEAR = 'total_debt_5_year'
    TOTAL_DEBT_3_YEAR = 'total_debt_3_year'
    TOTAL_DEBT_0_YEAR = 'total_debt_0_year'

    REVENUE_10_YEAR = 'revenue_10_year'
    REVENUE_5_YEAR = 'revenue_5_year'
    REVENUE_3_YEAR = 'revenue_3_year'
    REVENUE_0_YEAR = 'revenue_0_year'

    EARNINGS_10_YEAR = 'earnings_10_year'
    EARNINGS_5_YEAR = 'earnings_5_year'
    EARNINGS_3_YEAR = 'earnings_3_year'
    EARNINGS_0_YEAR = 'earnings_0_year'

    EQUITY_10_YEAR = 'equity_10_year'
    EQUITY_5_YEAR = 'equity_5_year'
    EQUITY_3_YEAR = 'equity_3_year'
    EQUITY_0_YEAR = 'equity_0_year'

    EQUITY_GROWTH = 'equity_growth'
    EARNINGS_GROWTH = 'earnings_growth'
    REVENUE_GROWTH = 'revenue_growth'
    CASH_GROWTH = 'cash_growth'

    # Other considerations
    HISTORIC_PE = 'historic_pe'
    TOTAL_DEBT = 'total_debt'
    MARGIN_OF_SAFETY = 'margin_of_safety'
    NUM_INCOME_STATEMENTS = 'num_income_statements'
    NUM_BALANCE_SHEETS = 'num_balance_sheets'
    NUM_CASH_FLOW_STATEMENTS = 'num_cash_flow_statements'

    INTRINSIC_VALUE = 'intrinsic_value'

    available_attributes = frozenset({TICKER,
                                      RETURN_ON_INVESTED_CAPITAL_10_YEAR,
                                      RETURN_ON_INVESTED_CAPITAL_5_YEAR,
                                      RETURN_ON_INVESTED_CAPITAL_1_YEAR,
                                      EQUITY_GROWTH,
                                      EQUITY_GROWTH_10_YEAR,
                                      EQUITY_GROWTH_5_YEAR,
                                      EQUITY_GROWTH_3_YEAR,
                                      EQUITY_GROWTH_1_YEAR,
                                      EARNINGS_GROWTH,
                                      EARNINGS_GROWTH_10_YEAR,
                                      EARNINGS_GROWTH_5_YEAR,
                                      EARNINGS_GROWTH_3_YEAR,
                                      EARNINGS_GROWTH_1_YEAR,
                                      REVENUE_GROWTH,
                                      REVENUE_GROWTH_10_YEAR,
                                      REVENUE_GROWTH_5_YEAR,
                                      REVENUE_GROWTH_3_YEAR,
                                      REVENUE_GROWTH_1_YEAR,
                                      CASH_GROWTH,
                                      OPERATING_CASH_GROWTH_10_YEAR,
                                      OPERATING_CASH_GROWTH_5_YEAR,
                                      OPERATING_CASH_GROWTH_3_YEAR,
                                      OPERATING_CASH_GROWTH_1_YEAR,
                                      HISTORIC_PE,
                                      TOTAL_DEBT,
                                      TOTAL_DEBT_10_YEAR,
                                      TOTAL_DEBT_5_YEAR,
                                      TOTAL_DEBT_3_YEAR,
                                      TOTAL_DEBT_0_YEAR,
                                      REVENUE_10_YEAR,
                                      REVENUE_5_YEAR,
                                      REVENUE_3_YEAR,
                                      REVENUE_0_YEAR,
                                      EARNINGS_10_YEAR,
                                      EARNINGS_5_YEAR,
                                      EARNINGS_3_YEAR,
                                      EARNINGS_0_YEAR,
                                      EQUITY_10_YEAR,
                                      EQUITY_5_YEAR,
                                      EQUITY_3_YEAR,
                                      EQUITY_0_YEAR,
                                      MARGIN_OF_SAFETY,
                                      NUM_INCOME_STATEMENTS,
                                      NUM_BALANCE_SHEETS,
                                      NUM_CASH_FLOW_STATEMENTS,
                                      INTRINSIC_VALUE
                                      })

    def __init__(self):
        pass

    def get(self, attr):
        return getattr(self, attr)

    def get_str(self, attr):
        return str(self.get(attr))

    def set_attr(self, attr, value):
        if attr not in self.available_attributes:
            raise AttributeError('Cannot set attribute ' + str(attr) + ' to CompanyReport, it is not a supported attribute')
        setattr(self, attr, value)

    def __str__(self):
        res = ''
        for attribute in sorted(self.available_attributes):
            res += attribute + ' : ' + str(getattr(self, attribute, 'missing')) + '\n'
        return res
