from clients.FinancialModelingPrepClient import FinancialModelingPrepClient
from dao.file_storage_dao import FileStorageDAO
import time
import datetime
import json


class DataRetriever:

    MAX_TICKERS = 10  # 10 is the max allowed for a single call

    @staticmethod
    def retrieve_all(tickers, time_to_live=0):
        DataRetriever.retrieve_financial_statements(tickers, time_to_live)
        DataRetriever.retrieve_key_ratios(tickers, time_to_live)

    @staticmethod
    def retrieve_tickers(time_to_live=0):
        # if the database has up to date information, then retrieve it from there.
        # otherwise, call FinancialModelingPrepClient

        try:
            tickers_info = FileStorageDAO.get_tickers()
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            tickers_info = None
            pass

        if tickers_info is None or time.time() - float(tickers_info.get('last_updated_date', 0)) >= time_to_live:
            tickers_info = FinancialModelingPrepClient.get_tickers()
            tickers_info['last_updated_date'] = time.time()
            tickers_info['last_updated_date_human'] = str(datetime.datetime.now())
            FileStorageDAO.save_tickers(tickers_info)

        tickers = []
        for datum in tickers_info['symbolsList']:
            tickers.append(datum['symbol'])

        return tickers

    @staticmethod
    def retrieve_key_ratios(tickers, time_to_live=0):
        return DataRetriever.retrieve_data(tickers, FileStorageDAO.get_key_ratios,
                                           FinancialModelingPrepClient.get_financial_ratios_batch,
                                           FileStorageDAO.save_key_ratios, time_to_live)

    @staticmethod
    def retrieve_financial_statements(tickers, time_to_live=0):
        DataRetriever.retrieve_income_statements(tickers, time_to_live)
        DataRetriever.retrieve_balance_sheets(tickers, time_to_live)
        DataRetriever.retrieve_cash_flow_statements(tickers, time_to_live)

    @staticmethod
    def retrieve_income_statements(tickers, time_to_live=0):
        return DataRetriever.retrieve_data(tickers, FileStorageDAO.get_income_statement,
                                           FinancialModelingPrepClient.get_income_statements_batch,
                                           FileStorageDAO.save_income_statement, time_to_live)

    @staticmethod
    def retrieve_balance_sheets(tickers, time_to_live=0):
        return DataRetriever.retrieve_data(tickers, FileStorageDAO.get_balance_sheet,
                                           FinancialModelingPrepClient.get_balance_sheets_batch,
                                           FileStorageDAO.save_balance_sheet, time_to_live)

    @staticmethod
    def retrieve_cash_flow_statements(tickers, time_to_live=0):
        return DataRetriever.retrieve_data(tickers, FileStorageDAO.get_cash_flow_statement,
                                           FinancialModelingPrepClient.get_cash_flow_statements_batch,
                                           FileStorageDAO.save_cash_flow_statement, time_to_live)

    # time_to_live is in seconds
    @staticmethod
    def retrieve_data(tickers, get_func, fetch_func, save_func, time_to_live=0):
        tickers_to_retrieve = []

        for ticker in tickers:
            try:
                info = get_func(ticker)
                if time.time() - float(info.get('last_updated_date', 0)) >= time_to_live:
                    tickers_to_retrieve.append(ticker)
            except (FileNotFoundError, json.decoder.JSONDecodeError):
                tickers_to_retrieve.append(ticker)
                continue
            except BaseException as e:
                print("Unexpected exception: " + str(e))
                tickers_to_retrieve.append(ticker)
                continue

        # if the database has up to date information, then retrieve it from there.
        # otherwise, call FinancialModelingPrepClient
        i = 0
        while i < len(tickers_to_retrieve):
            current_tickers = tickers_to_retrieve[i: i + DataRetriever.MAX_TICKERS]
            print('current tickers: ' + str(current_tickers))
            data = fetch_func(current_tickers)

            if len(data) != len(current_tickers):
                print('retrieve_income_statements: Data length does not match number of tickers')
                print('data length: ' + str(len(data)))
                print('tickers length: ' + str(len(tickers)))
                return False

            # save to the database
            for ticker, datum in zip(current_tickers, data):
                saved_datum = {'financials' : datum}
                saved_datum['last_updated_date'] = time.time()
                saved_datum['last_updated_date_human'] = str(datetime.datetime.now())
                save_func(ticker, saved_datum)

            i += DataRetriever.MAX_TICKERS

        return True


