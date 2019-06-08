from dao.file_storage_dao import FileStorageDAO
from scripts.utilities.utils import Utils
import time


class DataAnalyzer:

    @staticmethod
    def analyze_tickers(tickers, time_to_live=30 * 24 * 60 * 60):
        for ticker in tickers:
            try:
                DataAnalyzer.analyze_ticker(ticker, time_to_live)
            except Exception as e:
                print('Error analyzing ticker: ' + str(ticker))
                print(e)

    @staticmethod
    def analyze_ticker(ticker, time_to_live=30 * 24 * 60 * 60):

        try:
            analyzed_data = FileStorageDAO.get_anazlyed_data(ticker)
            if time.time() - float(analyzed_data.get('last_updated_date', 0)) < time_to_live:
                return
        except FileNotFoundError:
            # do nothing if no file exists
            pass

        organized_data = FileStorageDAO.get_organized_data(ticker)

        analyzed_data = {
            'earnings_score': DataAnalyzer.calculate_earnings_score(organized_data),
            'organized_data': organized_data,
            'last_updated_date': time.time(),
        }

        FileStorageDAO.save_analyzed_data(ticker, analyzed_data)

    @staticmethod
    def calculate_earnings_score(organized_data):
        increase_percentage = Utils.safe_cast(organized_data['earnings_increase_percentage'], float, 0)
        strict_increase_percentage = Utils.safe_cast(organized_data['earnings_strict_increase_percentage'], float, 0)

        return ((increase_percentage + strict_increase_percentage) / 2) * 100

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