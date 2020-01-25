from src.dao.file_storage_dao import FileStorageDAO


class FinancialStatementConverter:
    """
        Converts raw data (currently only from FinancialModelingPrep) into the corresponding business objects
    """

    @staticmethod
    def convert_income_statement_data(ticker):
        """
            Reads the raw income statement data for the given ticker and converts it into IncomeStatement objects

        :param ticker: the stock symbol
        :return: a list of income statement objects associated with the ticker that was input
        """
        json_data = FileStorageDAO.get_income_statement(ticker)
        # print(json_data)
        print(json_data['financials'])

        income_statements = []
        for income_statement_data in json_data['financials']:
            income_statements.push(FinancialStatementConverter.convert_income_statement_datum(income_statement_data))

    @staticmethod
    def convert_income_statement_datum(income_statement_data):
        pass


# For testing, remove later.
FinancialStatementConverter.convert_income_statement_data('AMZN')
