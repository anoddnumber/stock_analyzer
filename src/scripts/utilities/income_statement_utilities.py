class IncomeStatementUtilities:

    @staticmethod
    def get_earnings(income_statement):
        earnings = []
        for data in income_statement['financials']:
            eps = data['EPS']
            if eps is not "":
                earnings.append(float(eps))

        return earnings[::-1]

    @staticmethod
    def get_num_years(income_statement):
        return len(income_statement['financials'])
