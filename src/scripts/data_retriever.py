from clients.FinancialModelingPrepClient import FinancialModelingPrepClient
from dao.file_storage_dao import FileStorageDAO


class DataRetriever:

    @staticmethod
    def retrieve_financial_statements():
        pass

    @staticmethod
    def retrieve_income_statements(tickers):
        data = FinancialModelingPrepClient.get_income_statements_batch(tickers)

        if len(tickers) == 1:
            data = [data]
        else:
            data = data['financialStatementList']

        if len(data) != len(tickers):
            print('retrieve_income_statements: Data length does not match number of tickers')
            print('data length: ' + str(len(data)))
            print('tickers length: ' + str(len(tickers)))
            return

        for ticker, datum in zip(tickers, data):
            FileStorageDAO.save_income_statement(ticker, datum)

        return True

    @staticmethod
    def retrieve_balance_sheets():
        pass

    @staticmethod
    def retrieve_cash_flow_statements():
        pass


