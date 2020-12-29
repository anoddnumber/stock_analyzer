from dao.file_storage_dao import FileStorageDAO


class DataFilterer:

    """
    comparison_method is a function that is given the attribute and the value that should be filtered on
    It returns True if the attribute should be included in the result.
    """
    @staticmethod
    def filter(tickers, get_attr, comparsion_method, value):
        filtered_tickers = []
        full_filtered_tickers = []

        for ticker in tickers:
            try:
                analyzed_data = FileStorageDAO.get_analyzed_data(ticker)
            except FileNotFoundError:
                print('Did not find analyzed data for ' + ticker + '. Continuing')
                continue

            attr = get_attr(analyzed_data)
            if comparsion_method(attr, value):
                filtered_tickers.append(ticker)
                full_filtered_tickers.append({
                    'ticker': ticker,
                    'attr': attr,
                    'value': value,
                })

        return filtered_tickers, full_filtered_tickers

    @staticmethod
    def filter_reports(tickers, should_include):
        """
        Filters all of the company reports based off of a filter (a method) you pass in
        :param tickers: The list of stock symbols you want to run the filter on
        :param should_include: a method that returns true if it should be included in the resulting list. Takes a company report as the parameter
        :return: a list of stock symbols that pass the filter
        """
        filtered_tickers = []

        for ticker in tickers:
            try:
                report = FileStorageDAO.get_company_report(ticker)
            except FileNotFoundError:
                print('Did not find report for ' + ticker + '. Continuing')
                continue

            if should_include(report):
                filtered_tickers.append(ticker)

        return filtered_tickers

    """
        get_attr is a function that returns the attribute you want to filter by
        It takes the analyzed data as a parameter
    """
    @staticmethod
    def filter_greater_than(tickers, get_attr, value):
        return DataFilterer.filter(tickers, get_attr, lambda a, v: a > v, value)
