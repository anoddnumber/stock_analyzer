from dao.file_storage_dao import FileStorageDAO


class DataSorter:

    """
        get_attr is a method that returns the attribute you want to filter by
        It takes the analyzed data as a parameter
    """
    @staticmethod
    def sort(tickers, get_attr, reverse=False):
        data = []

        for ticker in tickers:
            analyzed_data = FileStorageDAO.get_analyzed_data(ticker)
            attr = get_attr(analyzed_data)
            data.append({
                'ticker': ticker,
                'attr': attr,
            })

        return sorted(data, key=lambda i: i['attr'], reverse=reverse)
