

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
    RETURN_ON_INVESTED_CAPITAL_3_YEAR = 'return_on_invested_capital_3_year'
    RETURN_ON_INVESTED_CAPITAL_1_YEAR = 'return_on_invested_capital_1_year'

    TOTAL_DEBT_10_YEAR = 'total_debt_10_year'
    TOTAL_DEBT_5_YEAR = 'total_debt_5_year'
    TOTAL_DEBT_3_YEAR = 'total_debt_3_year'
    TOTAL_DEBT_0_YEAR = 'total_debt_0_year'

    REVENUE = 'REVENUE'
    EARNINGS = 'EARNINGS'
    EQUITY = 'EQUITY'

    RETURN_ON_INVESTED_CAPITAL = 'return_on_invested_capital'
    EQUITY_GROWTH = 'equity_growth'
    EARNINGS_GROWTH = 'earnings_growth'
    REVENUE_GROWTH = 'revenue_growth'
    OPERATING_CASH_GROWTH = 'operating_cash_growth'

    # Other considerations
    HISTORIC_PE = 'historic_pe'
    TOTAL_DEBT = 'total_debt'
    MARGIN_OF_SAFETY = 'margin_of_safety'
    NUM_INCOME_STATEMENTS = 'num_income_statements'
    NUM_BALANCE_SHEETS = 'num_balance_sheets'
    NUM_CASH_FLOW_STATEMENTS = 'num_cash_flow_statements'
    EPS = 'EPS'
    EPS_DILUTED = 'EPS_DILUTED'
    SHARES_OUTSTANDING = 'SHARES_OUTSTANDING'
    RETURN_ON_EQUITY = 'RETURN_ON_EQUITY'
    DEBT_TO_EARNINGS = 'DEBT_TO_EARNINGS'
    PE_RATIOS = 'PE_RATIOS'
    AVERAGE_PE_RATIO = 'AVERAGE_PE_RATIO'


    INTRINSIC_VALUE = 'intrinsic_value'
    INTRINSIC_VALUE_GROWTH_RATE = 'intrinsic_value_growth_rate'
    CONSERVATIVE_INTRINSIC_VALUE = 'conservative_intrinsic_value'
    CONSERVATIVE_INTRINSIC_VALUE_GROWTH_RATE = 'conservative_intrinsic_value_growth_rate'

    available_attributes = frozenset({TICKER,
                                      RETURN_ON_INVESTED_CAPITAL,
                                      RETURN_ON_INVESTED_CAPITAL_10_YEAR,
                                      RETURN_ON_INVESTED_CAPITAL_5_YEAR,
                                      RETURN_ON_INVESTED_CAPITAL_3_YEAR,
                                      RETURN_ON_INVESTED_CAPITAL_1_YEAR,
                                      EQUITY_GROWTH,
                                      EARNINGS_GROWTH,
                                      REVENUE_GROWTH,
                                      OPERATING_CASH_GROWTH,
                                      HISTORIC_PE,
                                      TOTAL_DEBT,
                                      TOTAL_DEBT_10_YEAR,
                                      TOTAL_DEBT_5_YEAR,
                                      TOTAL_DEBT_3_YEAR,
                                      TOTAL_DEBT_0_YEAR,
                                      REVENUE,
                                      EARNINGS,
                                      EQUITY,
                                      MARGIN_OF_SAFETY,
                                      NUM_INCOME_STATEMENTS,
                                      NUM_BALANCE_SHEETS,
                                      NUM_CASH_FLOW_STATEMENTS,
                                      EPS,
                                      EPS_DILUTED,
                                      INTRINSIC_VALUE,
                                      INTRINSIC_VALUE_GROWTH_RATE,
                                      CONSERVATIVE_INTRINSIC_VALUE,
                                      CONSERVATIVE_INTRINSIC_VALUE_GROWTH_RATE,
                                      RETURN_ON_EQUITY,
                                      DEBT_TO_EARNINGS,
                                      SHARES_OUTSTANDING,
                                      PE_RATIOS,
                                      AVERAGE_PE_RATIO
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
