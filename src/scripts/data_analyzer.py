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
            analyzed_data = FileStorageDAO.get_analyzed_data(ticker)
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
        earnings_positive_percentage = Utils.safe_cast(organized_data['earnings_positive_percentage'], float, 0)
        num_years = Utils.safe_cast(organized_data['num_years'], int, 0)

        max_years = max(num_years, 10)

        values = [
            increase_percentage,
            strict_increase_percentage,
            earnings_positive_percentage,
            num_years / float(max_years)
        ]

        return Utils.average(values) * 100
