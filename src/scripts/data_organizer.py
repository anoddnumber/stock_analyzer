from dao.file_storage_dao import FileStorageDAO
from scripts.utilities.income_statement_utilities import IncomeStatementUtilities
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

        organized_data = {
            'earnings': earnings,
            'earnings_increase_percentage': DataOrganizer.calculate_increase_percentage(earnings),
            'earnings_strict_increase_percentage': DataOrganizer.calculate_strict_increase_percentage(earnings),
            'num_years': IncomeStatementUtilities.get_num_years(income_statement),
            'last_updated_date': time.time(),
        }

        FileStorageDAO.save_organized_data(ticker, organized_data)

    @staticmethod
    def calculate_increase_percentage(values):
        """ Calculates the percentage of times the value increases from the previous value. """
        if len(values) <= 1:
            return 0
        prev = values[0]
        num_increasing = 0
        for i in range(1, len(values)):
            value = values[i]
            if value > prev:
                num_increasing += 1
            prev = value

        return num_increasing / (len(values) - 1.0)

    @staticmethod
    def calculate_strict_increase_percentage(values):
        """Calculates the percentage of times the value increases from the previous maximum. """
        if len(values) <= 1:
            return 0
        max_value = values[0]
        num_increasing = 0
        for i in range(1, len(values)):
            value = values[i]
            if value > max_value:
                num_increasing += 1
                max_value = value

        return num_increasing / (len(values) - 1.0)