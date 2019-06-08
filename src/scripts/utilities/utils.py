class Utils:

    @staticmethod
    def average(values):
        if len(values) == 0:
            return 0
        return float(sum(values)) / len(values)

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
