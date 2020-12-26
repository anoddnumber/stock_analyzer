import json
import os
from business_objects.company_report import CompanyReport


class FileStorageDAO:
    """
        DAO to retrieve and save information. We will need to modify this when we add more sources in the future.
        We will need to have a directory per source.
    """

    home_dir = os.path.expanduser("~")
    ROOT_DIR = home_dir + '/Documents/work/workspace/stock_analyzer/'
    DATA_DIR = ROOT_DIR + 'data/'
    ANALYSIS_DIR = DATA_DIR + 'analysis/'
    ORGANIZED_DATA_DIR = DATA_DIR + 'organized_data/'

    FINANCIAL_STATEMENTS_DIR = DATA_DIR + 'financial_statements/'
    INCOME_STATEMENTS_DIR = FINANCIAL_STATEMENTS_DIR + 'income_statements/'
    BALANCE_SHEET_DIR = FINANCIAL_STATEMENTS_DIR + 'balance_sheets/'
    CASH_FLOW_STATEMENTS_DIR = FINANCIAL_STATEMENTS_DIR + 'cash_flow_statements/'

    KEY_RATIOS_DIR = DATA_DIR + 'key_ratios/'
    COMPANY_REPORTS_DIR = DATA_DIR + 'company_reports/'

    @staticmethod
    def get_financial_statements(ticker):
        pass

    @staticmethod
    def get_key_ratios(ticker):
        return FileStorageDAO.get_data(ticker, FileStorageDAO.KEY_RATIOS_DIR)

    @staticmethod
    def get_income_statement(ticker):
        return FileStorageDAO.get_data(ticker, FileStorageDAO.INCOME_STATEMENTS_DIR)

    @staticmethod
    def get_balance_sheet(ticker):
        return FileStorageDAO.get_data(ticker, FileStorageDAO.BALANCE_SHEET_DIR)

    @staticmethod
    def get_cash_flow_statement(ticker):
        return FileStorageDAO.get_data(ticker, FileStorageDAO.CASH_FLOW_STATEMENTS_DIR)

    @staticmethod
    def get_organized_data(ticker):
        return FileStorageDAO.get_data(ticker, FileStorageDAO.ORGANIZED_DATA_DIR)

    @staticmethod
    def get_analyzed_data(ticker):
        return FileStorageDAO.get_data(ticker, FileStorageDAO.ANALYSIS_DIR)

    @staticmethod
    def get_data(ticker, directory):
        return json.load(open(directory + ticker + '.json', 'r'))

    @staticmethod
    def save_key_ratios(ticker, json_obj):
        FileStorageDAO._save_json(FileStorageDAO.KEY_RATIOS_DIR + ticker + '.json', json_obj)

    @staticmethod
    def save_income_statement(ticker, json_obj):
        FileStorageDAO._save_json(FileStorageDAO.INCOME_STATEMENTS_DIR + ticker + '.json', json_obj)

    @staticmethod
    def save_balance_sheet(ticker, json_obj):
        FileStorageDAO._save_json(FileStorageDAO.BALANCE_SHEET_DIR + ticker + '.json', json_obj)

    @staticmethod
    def save_cash_flow_statement(ticker, json_obj):
        FileStorageDAO._save_json(FileStorageDAO.CASH_FLOW_STATEMENTS_DIR + ticker + '.json', json_obj)

    @staticmethod
    def save_organized_data(ticker, json_obj):
        FileStorageDAO._save_json(FileStorageDAO.ORGANIZED_DATA_DIR + ticker + '.json', json_obj)

    @staticmethod
    def save_analyzed_data(ticker, json_obj):
        FileStorageDAO._save_json(FileStorageDAO.ANALYSIS_DIR + ticker + '.json', json_obj)

    @staticmethod
    def save_report(company_report):
        print('\n\ncompany report:\n' + str(company_report))
        ticker = company_report.get(CompanyReport.TICKER)
        file = open(FileStorageDAO.COMPANY_REPORTS_DIR + ticker + '.txt', "w")
        file.write(ticker + '\n\n')
        file.write('Number of Income Statements: ' + company_report.get_str(CompanyReport.NUM_INCOME_STATEMENTS) + '\n')
        file.write('Number of Balance Sheets: ' + company_report.get_str(CompanyReport.NUM_BALANCE_SHEETS) + '\n')
        file.write('Number of Cash Flow Statements: ' + company_report.get_str(CompanyReport.NUM_CASH_FLOW_STATEMENTS) + '\n\n\n')
        file.write('# Big 5\n')
        file.write('ROIC 1 Year: ' + company_report.get_str(CompanyReport.RETURN_ON_INVESTED_CAPITAL_1_YEAR) + '\n')
        file.write('Equity Growth: ' + company_report.get_str(CompanyReport.EQUITY_GROWTH) + '\n')
        file.write('Earnings Growth: ' + company_report.get_str(CompanyReport.EARNINGS_GROWTH) + "\n")
        file.write('Revenue Growth: ' + company_report.get_str(CompanyReport.REVENUE_GROWTH) + "\n")
        file.write('Cash Growth: ' + company_report.get_str(CompanyReport.CASH_GROWTH) + "\n")
        file.close()

    @staticmethod
    def _make_directories():
        paths = [FileStorageDAO.ROOT_DIR, FileStorageDAO.DATA_DIR, FileStorageDAO.FINANCIAL_STATEMENTS_DIR,
                 FileStorageDAO.INCOME_STATEMENTS_DIR, FileStorageDAO.BALANCE_SHEET_DIR,
                 FileStorageDAO.CASH_FLOW_STATEMENTS_DIR, FileStorageDAO.KEY_RATIOS_DIR]

        for path in paths:
            if not os.path.isdir(path):
                os.mkdir(path)

    @staticmethod
    def _save_json(file_path, json_obj):
        file = open(file_path, 'w')
        file.write(json.dumps(json_obj, indent=2))
        file.close()
