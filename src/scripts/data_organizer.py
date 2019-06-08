from dao.file_storage_dao import FileStorageDAO
from scripts.utilities.income_statement_utilities import IncomeStatementUtilities
from scripts.utilities.utils import Utils
import time


class DataOrganizer:

    @staticmethod
    def organize_tickers(tickers, time_to_live=30 * 24 * 60 * 60):
        for ticker in tickers:
            try:
                DataOrganizer.organize_ticker(ticker, time_to_live)
            except Exception as e:
                print('Error organizing ticker: ' + str(ticker))
                print(e)

    @staticmethod
    def organize_ticker(ticker, time_to_live=30 * 24 * 60 * 60):

        try:
            info = FileStorageDAO.get_organized_data(ticker)
            if time.time() - float(info.get('last_updated_date', 0)) < time_to_live:
                return
        except FileNotFoundError:
            # do nothing
            pass

        income_statement = FileStorageDAO.get_income_statement(ticker)
        # balance_sheet = FileStorageDAO.get_balance_sheet(ticker)
        # cash_flow_statement = FileStorageDAO.get_cash_flow_statement(ticker)

        earnings = IncomeStatementUtilities.get_earnings(income_statement)
        revenue = IncomeStatementUtilities.get_revenue(income_statement)

        organized_data = {
            'average_earnings': Utils.average(earnings),
            'earnings': earnings,
            'earnings_positive_percentage': Utils.calculate_percent_positive(earnings),
            'earnings_increase_percentage': Utils.calculate_increase_percentage(earnings),
            'earnings_strict_increase_percentage': Utils.calculate_strict_increase_percentage(earnings),
            'average_revenue': Utils.average(revenue),
            'revenue': revenue,
            'revenue_positive_percentage': Utils.calculate_percent_positive(revenue),
            'revenue_increase_percentage': Utils.calculate_increase_percentage(revenue),
            'revenue_strict_increase_percentage': Utils.calculate_strict_increase_percentage(revenue),
            'num_years': IncomeStatementUtilities.get_num_years(income_statement),
            'last_updated_date': time.time(),
        }

        FileStorageDAO.save_organized_data(ticker, organized_data)
