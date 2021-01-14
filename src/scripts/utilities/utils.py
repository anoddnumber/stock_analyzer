import math
from definitions import ROOT_DIR


class Utils:
    API_FILE_NAME = 'API_KEY.txt'

    @staticmethod
    def get_api_key():
        api_file = open(ROOT_DIR + '/' + Utils.API_FILE_NAME, "r")
        api_key = api_file.readline()
        api_file.close()
        return api_key

    @staticmethod
    def remove_negative_numbers(numbers):
        return [ele for ele in numbers if ele > 0]

    @staticmethod
    def average(values):
        if len(values) == 0:
            return 0
        return float(sum(values)) / len(values)

    @staticmethod
    def weighted_average(data_points):
        if len(data_points) == 0:
            return 0

        total = 0.0
        total_weight = 0
        for point in data_points:
            total_weight += point.weight
            total += point.weight * point.value

        if total_weight == 0:
            return 0

        return total / total_weight

    @staticmethod
    def safe_cast(val, to_type, default=None):
        try:
            return to_type(val)
        except (ValueError, TypeError):
            return default

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

    @staticmethod
    def calculate_percent_positive(values):
        """Calculates the percentage of times the value increases from the previous maximum. """
        if len(values) <= 1:
            return 0
        num_positive = 0
        for value in values:
            if value > 0:
                num_positive += 1

        return num_positive / len(values)

    @staticmethod
    def calculate_yoy_return(starting_value, ending_value, num_years=1):
        try:
            if starting_value <= 0 or ending_value <= 0:
                return None
            return math.exp(math.log(ending_value * 1.0 / starting_value) / num_years) - 1
        except (ValueError, ZeroDivisionError):
            return None

    @staticmethod
    def calculate_intrinsic_value(eps, growth_rate, future_pe, minimum_acceptable_rate_of_return=.15):
        """

        :param eps:
        :param growth_rate: .25 means 25% growth rate
        :param future_pe:
        :param minimum_acceptable_rate_of_return: .25 means 25% growth rate
        :return:
        """
        num_years = 10
        future_eps = eps * math.pow(1 + growth_rate, num_years)
        future_val = future_eps * future_pe
        intrinsic_val = future_val / math.pow(1 + minimum_acceptable_rate_of_return, num_years)
        return intrinsic_val

    @staticmethod
    def calculate_payback_time(price, shares_outstanding, growth_rate, earnings_ttm):
        """
        :param price: the price you will buy at
        :param shares_outstanding: the number of shares outstanding for the company
        :param growth_rate: the growth rate of the earnings
        :param earnings_ttm: how many earnings the company made in the last 12 months (ttm = trailing twelve months)
        :return: the number of years it will take for the earnings to equal the amount you paid for the company
        """
        if price < 0 or shares_outstanding < 0 or growth_rate <= 0 or earnings_ttm <= 0:
            return -1

        num_years = 0
        target = price * shares_outstanding
        next_earnings = earnings_ttm
        while next_earnings < target:
            target -= next_earnings
            num_years += 1
            next_earnings *= growth_rate

        num_years += target / next_earnings
        return num_years