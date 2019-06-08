class IncomeStatementUtilities:

    @staticmethod
    def get_earnings(income_statement):
        return IncomeStatementUtilities.get_attr_list(income_statement, 'EPS')

    @staticmethod
    def get_revenue(income_statement):
        return IncomeStatementUtilities.get_attr_list(income_statement, 'Revenue')

    @staticmethod
    def get_attr_list(income_statement, attr):
        attributes = []
        for data in income_statement['financials']:
            attribute = data[attr]
            if attribute is not "":
                attributes.append(float(attribute))

        return attributes[::-1]

    @staticmethod
    def get_num_years(income_statement):
        return len(income_statement['financials'])
