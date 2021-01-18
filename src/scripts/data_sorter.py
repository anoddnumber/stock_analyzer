from dao.file_storage_dao import FileStorageDAO
from business_objects.company_report import CompanyReport


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


    @staticmethod
    def sort_reports(tickers, sort_method):
        """
        Filters all of the company reports based off of a filter (a method) you pass in
        :param tickers: The list of stock symbols you want to run the filter on
        :param sortmethod: a method that returns true if it should be included in the resulting list. Takes a company report as the parameter
        :return: a list of stock symbols that pass the filter
        """
        if sort_method is None:
            sort_method = DataSorter.default_sort_report_method
        return sorted(tickers, sort_method)

    @staticmethod
    def default_sort_report_method():
        def default_sort_method(ticker):
            try:
                company_report = FileStorageDAO.get_company_report(ticker)
            except FileNotFoundError:
                print('Did not find report for ' + ticker + ' when sorting.')
                return 0

            roic_list = company_report.get(CompanyReport.RETURN_ON_INVESTED_CAPITAL)
            equity_growth = company_report.get(CompanyReport.EQUITY_GROWTH)
            earnings_growth = company_report.get(CompanyReport.EARNINGS_GROWTH)
            revenue_growth = company_report.get(CompanyReport.REVENUE_GROWTH)
            operating_cash_flow_growth = company_report.get(CompanyReport.OPERATING_CASH_GROWTH)

            if len(roic_list) < 1 or len(equity_growth) < 3 or len(earnings_growth) < 3 or len(
                    revenue_growth) < 3 or len(operating_cash_flow_growth) < 3:
                return 0

            return roic_list[0] + equity_growth[2] + earnings_growth[2] + revenue_growth[2] + operating_cash_flow_growth[2]
        return default_sort_method
