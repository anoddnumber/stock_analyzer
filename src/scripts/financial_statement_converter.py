from src.dao.file_storage_dao import FileStorageDAO
from src.business_objects.income_statement import IncomeStatement
from src.client_info.financial_modeling_prep_info import FinancialModelingPrepInfo


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

        income_statements = []
        for income_statement_data in json_data['financials']:
            income_statements.append(IncomeStatement(ticker,
                                                     FinancialModelingPrepInfo.income_statement_object_to_json_mapping,
                                                     income_statement_data))

        return income_statements