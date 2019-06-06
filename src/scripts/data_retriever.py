from clients.FinancialModelingPrepClient import FinancialModelingPrepClient
from dao.file_storage_dao import FileStorageDAO
import time


class DataRetriever:

    MAX_TICKERS = 10  # 10 is the max allowed for a single call

    @staticmethod
    def retrieve_financial_statements():
        pass

    @staticmethod
    def retrieve_income_statements(tickers):
        tickers_to_retrieve = []
        thirty_days_in_seconds = 30 * 24 * 60 * 60

        for ticker in tickers:
            try:
                info = FileStorageDAO.get_income_statement(ticker)
                if time.time() - float(info.get('last_updated_date', 0)) >= thirty_days_in_seconds:
                    tickers_to_retrieve.append(ticker)
            except FileNotFoundError:
                continue

        # if the database has up to date information, then retrieve it from there.
        # otherwise, call FinancialModelingPrepClient
        i = 0
        while i < len(tickers_to_retrieve):
            current_tickers = tickers_to_retrieve[i: i + DataRetriever.MAX_TICKERS]
            print(current_tickers)
            data = FinancialModelingPrepClient.get_income_statements_batch(current_tickers)

            if len(current_tickers) == 1:
                data = [data]
            else:
                data = data['financialStatementList']

            if len(data) != len(current_tickers):
                print('retrieve_income_statements: Data length does not match number of tickers')
                print('data length: ' + str(len(data)))
                print('tickers length: ' + str(len(tickers)))
                return

            # save to the database
            for ticker, datum in zip(current_tickers, data):
                datum['last_updated_date'] = time.time()
                FileStorageDAO.save_income_statement(ticker, datum)

            i += DataRetriever.MAX_TICKERS
            # time.sleep(1)

        return True

    @staticmethod
    def retrieve_balance_sheets():
        pass

    @staticmethod
    def retrieve_cash_flow_statements():
        pass


