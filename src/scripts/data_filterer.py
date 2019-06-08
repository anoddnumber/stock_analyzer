from dao.file_storage_dao import FileStorageDAO


class DataFilterer:

    """
        get_attr is a method that returns the attribute you want to filter by
        It takes the analyzed data as a parameter
    """
    @staticmethod
    def filter_greater_than(tickers, get_attr, value):
        filtered_tickers = []
        full_filtered_tickers = []

        for ticker in tickers:
            analyzed_data = FileStorageDAO.get_analyzed_data(ticker)
            attr = get_attr(analyzed_data)
            if attr > value:
                filtered_tickers.append(ticker)
                full_filtered_tickers.append({
                    'ticker': ticker,
                    'attr': attr,
                })

        return filtered_tickers, full_filtered_tickers
