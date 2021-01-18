import json
import os
from business_objects.company_report import CompanyReport
import math
from scripts.utilities.utils import Utils


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
    KEY_RATIOS_TTM_DIR =  DATA_DIR + 'key_ratios_ttm/'
    COMPANY_QUOTES_DIR = DATA_DIR + 'company_quotes/'
    COMPANY_REPORTS_DIR = DATA_DIR + 'company_reports/'
    TICKERS_FILE = DATA_DIR + 'tickers.json'

    @staticmethod
    def get_financial_statements(ticker):
        pass

    @staticmethod
    def get_company_report(ticker):
        return FileStorageDAO.get_data(ticker, FileStorageDAO.COMPANY_REPORTS_DIR)

    @staticmethod
    def get_tickers():
        return json.load(open(FileStorageDAO.TICKERS_FILE, 'r'))

    @staticmethod
    def get_key_ratios(ticker):
        return FileStorageDAO.get_data(ticker, FileStorageDAO.KEY_RATIOS_DIR)

    @staticmethod
    def get_key_ratios_ttm(ticker):
        return FileStorageDAO.get_data(ticker, FileStorageDAO.KEY_RATIOS_TTM_DIR)

    @staticmethod
    def get_company_quote(ticker):
        return FileStorageDAO.get_data(ticker, FileStorageDAO.COMPANY_QUOTES_DIR)

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
    def save_tickers(json_obj):
        FileStorageDAO._save_json(FileStorageDAO.TICKERS_FILE, json_obj)

    @staticmethod
    def save_key_ratios(ticker, json_obj):
        FileStorageDAO._save_json(FileStorageDAO.KEY_RATIOS_DIR + ticker + '.json', json_obj)

    @staticmethod
    def save_key_ratios_ttm(ticker, json_obj):
        FileStorageDAO._save_json(FileStorageDAO.KEY_RATIOS_TTM_DIR + ticker + '.json', json_obj)

    @staticmethod
    def save_company_quote_batch(json_objs):
        for json_obj in json_objs:
            ticker = json_obj['symbol']
            FileStorageDAO._save_json(FileStorageDAO.COMPANY_QUOTES_DIR + ticker + '.json', json_obj)

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
        file.write('Number of Cash Flow Statements: ' + company_report.get_str(CompanyReport.NUM_CASH_FLOW_STATEMENTS) + '\n')
        file.write('Data is from the most recent year first in lists - [year1, year2, year3, ...] where year1 is the most recent year\n\n\n')
        file.write('Dates: ' + company_report.get_str(CompanyReport.DATES) + '\n')

        file.write('# Big 5\n')
        file.write('ROIC: ' + str(company_report.get(CompanyReport.RETURN_ON_INVESTED_CAPITAL)) + '\n\n')
        file.write('Equity Growth: ' + str(company_report.get(CompanyReport.EQUITY_GROWTH)) + '\n\n')
        file.write('Earnings Growth: ' + str(company_report.get(CompanyReport.EARNINGS_GROWTH)) + '\n\n')
        file.write('Revenue Growth: ' + str(company_report.get(CompanyReport.REVENUE_GROWTH)) + '\n\n')
        file.write('Operating Cash Growth: ' + str(company_report.get(CompanyReport.OPERATING_CASH_GROWTH)) + '\n\n')

        # 0 year just means the most recent year that has data
        file.write('\nOther important metrics\n')
        file.write('Debt: ' + str(company_report.get(CompanyReport.TOTAL_DEBT)) + '\n\n')

        file.write('Equity: ' + str(company_report.get(CompanyReport.EQUITY)) + '\n\n')
        file.write('Earnings: ' + str(company_report.get(CompanyReport.EARNINGS)) + '\n\n')
        file.write('Revenue: ' + str(company_report.get(CompanyReport.REVENUE)) + '\n\n')
        file.write('Return on Equity: ' + str(company_report.get(CompanyReport.RETURN_ON_EQUITY)) + '\n\n')
        file.write('PE Ratios: ' + str(company_report.get(CompanyReport.PE_RATIOS)) + '\n\n')
        file.write('Debt to Earnings: ' + str(company_report.get(CompanyReport.DEBT_TO_EARNINGS)) + '\n\n')
        file.write('Shares Outstanding: ' + str(company_report.get(CompanyReport.SHARES_OUTSTANDING)) + '\n\n')
        # TODO: Add payback time

        file.write('\nEPS: ' + company_report.get_str(CompanyReport.EPS) + '\n')
        file.write('EPS Diluted: ' + company_report.get_str(CompanyReport.EPS_DILUTED) + '\n\n')
        file.write('EPS TTM: ' + company_report.get_str(CompanyReport.EPS_TTM) + '\n\n')

        file.write('Growth rate for intrinsic value: ' + company_report.get_str(CompanyReport.INTRINSIC_VALUE_GROWTH_RATE) + '\n')
        file.write('PE for intrinsic value (average of positive PEs): ' + company_report.get_str(CompanyReport.AVERAGE_PE_RATIO) + '\n\n')

        file.write('Growth rate for conservative intrinsic value: ' + company_report.get_str(CompanyReport.CONSERVATIVE_INTRINSIC_VALUE_GROWTH_RATE) + '\n')
        file.write('PE for conservative intrinsic value: 15\n\n')

        file.write('\nIntrinsic value: ' + company_report.get_str(CompanyReport.INTRINSIC_VALUE))
        file.write('\nConservative intrinsic value: ' + company_report.get_str(CompanyReport.CONSERVATIVE_INTRINSIC_VALUE))

        file.write('\nIntrinsic value using TTM EPS: ' + company_report.get_str(CompanyReport.INTRINSIC_VALUE_USING_TTM_EPS))
        file.write('\nConservative intrinsic value using TTM EPS: ' + company_report.get_str(CompanyReport.CONSERVATIVE_INTRINSIC_VALUE_USING_TTM_EPS))



        # Payback time
        shares_outstanding = company_report.get(CompanyReport.SHARES_OUTSTANDING)
        growth_rate = company_report.get(CompanyReport.INTRINSIC_VALUE_GROWTH_RATE)
        eps = company_report.get(CompanyReport.EPS)
        intrinsic_value = company_report.get(CompanyReport.INTRINSIC_VALUE)

        file.write('\n\nPayback time with last year\'s earnings (not TTM):\n')
        file.write('EPS: ' + str(eps) + '\n')
        file.write('Shares Outstanding: ' + str(shares_outstanding) + '\n')
        file.write('Growth rate for intrinsic value: ' + company_report.get_str(
            CompanyReport.INTRINSIC_VALUE_GROWTH_RATE) + '\n')
        file.write('Calculated Payback Time with intrinsic value ' + str(intrinsic_value)
                   + ': ' + Utils.calculate_payback_time(intrinsic_value, shares_outstanding, growth_rate, eps))
        file.write('Calculated Payback Time with intrinsic value ' + str(intrinsic_value)
                   + ': ' + Utils.calculate_payback_time(intrinsic_value, shares_outstanding, growth_rate, eps))

        FileStorageDAO.write_payback_time_table(company_report.get(CompanyReport.EPS), shares_outstanding,
                                                growth_rate, file)


        file.write('\n\nConservative Payback time:\n')

        file.close()

    @staticmethod
    def write_payback_time_table(eps, shares_outstanding, growth_rate, file, num_years=20):
        file.write('Year, Estimated Earnings, Cumulative Earnings')

        cumulative_earnings = 0
        for year in range(0, num_years):
            year_earnings = eps * shares_outstanding * math.pow(growth_rate, num_years)
            cumulative_earnings += year_earnings
            file.write('0, ' + str(year_earnings) + ', ' + str(cumulative_earnings) + '\n')

    @staticmethod
    def _make_directories():
        paths = [FileStorageDAO.ROOT_DIR, FileStorageDAO.DATA_DIR, FileStorageDAO.FINANCIAL_STATEMENTS_DIR,
                 FileStorageDAO.INCOME_STATEMENTS_DIR, FileStorageDAO.BALANCE_SHEET_DIR,
                 FileStorageDAO.CASH_FLOW_STATEMENTS_DIR, FileStorageDAO.KEY_RATIOS_DIR, FileStorageDAO.COMPANY_QUOTES_DIR,
                 FileStorageDAO.KEY_RATIOS_TTM_DIR]

        for path in paths:
            if not os.path.isdir(path):
                os.mkdir(path)

    @staticmethod
    def _save_json(file_path, json_obj):
        file = open(file_path, 'w')
        file.write(json.dumps(json_obj, indent=2))
        file.close()
