import json
import os


class FileStorageDAO:

    ROOT_DIR = '../'
    DATA_DIR = ROOT_DIR + 'data/'
    ANALYSIS_DIR = DATA_DIR + 'analysis/'
    ORGANIZED_DATA_DIR = DATA_DIR + 'organized_data/'
    FINANCIAL_STATEMENTS_DIR = DATA_DIR + 'financial_statements/'
    INCOME_STATEMENTS_DIR = FINANCIAL_STATEMENTS_DIR + 'income_statements/'
    BALANCE_SHEET_DIR = FINANCIAL_STATEMENTS_DIR + 'balance_sheets/'
    CASH_FLOW_STATEMENTS_DIR = FINANCIAL_STATEMENTS_DIR + 'cash_flow_statements/'

    @staticmethod
    def get_tickers():
        tickers_file = open(FileStorageDAO.DATA_DIR + 'tickers.txt', 'r')
        tickers = []

        for i, line in enumerate(tickers_file):
            if i != 0:
                tickers.append(line[0:line.index('|')])
        return tickers

    @staticmethod
    def get_financial_statements(ticker):
        pass

    @staticmethod
    def get_income_statement(ticker):
        income_statement = open(FileStorageDAO.INCOME_STATEMENTS_DIR + ticker + '.json', 'r')
        return json.load(income_statement)

    @staticmethod
    def get_balance_sheet(ticker):
        income_statement = open(FileStorageDAO.BALANCE_SHEET_DIR + ticker + '.json', 'r')
        return json.load(income_statement)

    @staticmethod
    def get_cash_flow_statement(ticker):
        income_statement = open(FileStorageDAO.CASH_FLOW_STATEMENTS_DIR + ticker + '.json', 'r')
        return json.load(income_statement)

    @staticmethod
    def save_income_statement(ticker, json_obj):
        FileStorageDAO._save(FileStorageDAO.INCOME_STATEMENTS_DIR + ticker + '.json', json_obj)

    @staticmethod
    def save_balance_sheet(ticker, json_obj):
        FileStorageDAO._save(FileStorageDAO.BALANCE_SHEET_DIR + ticker + '.json', json_obj)

    @staticmethod
    def save_cash_flow_statement(ticker, json_obj):
        FileStorageDAO._save(FileStorageDAO.CASH_FLOW_STATEMENTS_DIR + ticker + '.json', json_obj)

    @staticmethod
    def save_organized_data(ticker, json_obj):
        FileStorageDAO._save(FileStorageDAO.ORGANIZED_DATA_DIR + ticker + '.json', json_obj)

    @staticmethod
    def _make_directories():
        paths = [FileStorageDAO.ROOT_DIR, FileStorageDAO.DATA_DIR, FileStorageDAO.FINANCIAL_STATEMENTS_DIR,
                 FileStorageDAO.INCOME_STATEMENTS_DIR, FileStorageDAO.BALANCE_SHEET_DIR,
                 FileStorageDAO.CASH_FLOW_STATEMENTS_DIR]

        for path in paths:
            if not os.path.isdir(path):
                os.mkdir(path)

    @staticmethod
    def _save(file_path, json_obj):
        file = open(file_path, 'w')
        file.write(json.dumps(json_obj, indent=2))
        file.close()