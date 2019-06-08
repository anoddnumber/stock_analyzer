from clients.FinancialModelingPrepClient import FinancialModelingPrepClient
from dao.file_storage_dao import FileStorageDAO
import time


class DataRetriever:

    MAX_TICKERS = 10  # 10 is the max allowed for a single call

    @staticmethod
    def retrieve_financial_statements(tickers):
        DataRetriever.retrieve_income_statements(tickers)
        DataRetriever.retrieve_balance_sheets(tickers)
        DataRetriever.retrieve_cash_flow_statements(tickers)

    @staticmethod
    def retrieve_income_statements(tickers):
        return DataRetriever.retrieve_data(tickers, FileStorageDAO.get_income_statement,
                                           FinancialModelingPrepClient.get_income_statements_batch,
                                           FileStorageDAO.save_income_statement)

    @staticmethod
    def retrieve_balance_sheets(tickers):
        return DataRetriever.retrieve_data(tickers, FileStorageDAO.get_balance_sheet,
                                           FinancialModelingPrepClient.get_balance_sheets_batch,
                                           FileStorageDAO.save_balance_sheet)

    @staticmethod
    def retrieve_cash_flow_statements(tickers):
        return DataRetriever.retrieve_data(tickers, FileStorageDAO.get_cash_flow_statement,
                                           FinancialModelingPrepClient.get_cash_flow_statements_batch,
                                           FileStorageDAO.save_cash_flow_statement)

    @staticmethod
    def retrieve_data(tickers, get_func, fetch_func, save_func, time_to_live=30 * 24 * 60 * 60):
        tickers_to_retrieve = []

        for ticker in tickers:
            try:
                info = get_func(ticker)
                if time.time() - float(info.get('last_updated_date', 0)) >= time_to_live:
                    tickers_to_retrieve.append(ticker)
            except FileNotFoundError:
                tickers_to_retrieve.append(ticker)
                continue

        # if the database has up to date information, then retrieve it from there.
        # otherwise, call FinancialModelingPrepClient
        i = 0
        while i < len(tickers_to_retrieve):
            current_tickers = tickers_to_retrieve[i: i + DataRetriever.MAX_TICKERS]
            print(current_tickers)
            data = fetch_func(current_tickers)

            if len(data) != len(current_tickers):
                print('retrieve_income_statements: Data length does not match number of tickers')
                print('data length: ' + str(len(data)))
                print('tickers length: ' + str(len(tickers)))
                return False

            # save to the database
            for ticker, datum in zip(current_tickers, data):
                datum['last_updated_date'] = time.time()
                save_func(ticker, datum)

            i += DataRetriever.MAX_TICKERS

        return True


