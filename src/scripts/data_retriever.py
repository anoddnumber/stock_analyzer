from clients.FinancialModelingPrepClient import FinancialModelingPrepClient
from dao.file_storage_dao import FileStorageDAO


class DataRetriever:

    @staticmethod
    def retrieve_financial_statements():
        pass

    @staticmethod
    def retrieve_income_statements(tickers):
        data = FinancialModelingPrepClient.get_income_statements_batch(tickers)
        # print(data)
        FileStorageDAO.save_income_statement(tickers[0], data)
        return True

    @staticmethod
    def retrieve_balance_sheets():
        pass

    @staticmethod
    def retrieve_cash_flow_statements():
        pass


