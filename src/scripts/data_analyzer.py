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
        earnings_score = DataAnalyzer.calculate_earnings_score(organized_data)
        revenue_score = DataAnalyzer.calculate_revenue_score(organized_data)
        growth_score = DataAnalyzer.calculate_growth_score(organized_data)
        overall_score = Utils.average([earnings_score, revenue_score, growth_score])

        analyzed_data = {
            'price_target': DataAnalyzer.calculate_price_target(organized_data),
            'earnings_score': earnings_score,
            'revenue_score': revenue_score,
            'growth_score': growth_score,
            'overall_score': overall_score,
            'organized_data': organized_data,
            'last_updated_date': time.time(),
        }

        FileStorageDAO.save_analyzed_data(ticker, analyzed_data)

    @staticmethod
    def calculate_price_target(organized_data):
        if len(organized_data['earnings']) <= 0:
            return 0
        return organized_data['earnings'][-1] * 15

    @staticmethod
    def calculate_growth_score(organized_data):
        if organized_data['earnings_growth'] is None:
            return 0

        growth = organized_data['earnings_growth'] * 100

        if growth <= 0:
            return 0
        if growth <= 10:
            return growth * 8
        if growth <= 15:
            return 90
        return 100

    @staticmethod
    def calculate_earnings_score(organized_data):
        increase_percentage = Utils.safe_cast(organized_data['earnings_increase_percentage'], float, 0)
        strict_increase_percentage = Utils.safe_cast(organized_data['earnings_strict_increase_percentage'], float, 0)
        positive_percentage = Utils.safe_cast(organized_data['earnings_positive_percentage'], float, 0)
        num_years = Utils.safe_cast(organized_data['num_years'], int, 0)

        max_years = max(num_years, 10)

        values = [
            increase_percentage,
            strict_increase_percentage,
            positive_percentage,
            num_years / float(max_years)
        ]

        return Utils.average(values) * 100

    @staticmethod
    def calculate_revenue_score(organized_data):
        increase_percentage = Utils.safe_cast(organized_data['revenue_increase_percentage'], float, 0)
        strict_increase_percentage = Utils.safe_cast(organized_data['revenue_strict_increase_percentage'], float, 0)
        positive_percentage = Utils.safe_cast(organized_data['revenue_positive_percentage'], float, 0)
        num_years = Utils.safe_cast(organized_data['num_years'], int, 0)

        max_years = max(num_years, 10)

        values = [
            increase_percentage,
            strict_increase_percentage,
            positive_percentage,
            num_years / float(max_years)
        ]

        return Utils.average(values) * 100