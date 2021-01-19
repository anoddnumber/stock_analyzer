from dao.file_storage_dao import FileStorageDAO
from business_objects.company_report import CompanyReport
import functools


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
    def sort_reports(tickers, sort_method=None):
        """
        Filters all of the company reports based off of a filter (a method) you pass in
        :param tickers: The list of stock symbols you want to run the filter on
        :param sort_method: a method that returns a number that determines the sort order
        :return: a list of stock symbols that pass the filter
        """
        if sort_method is None:
            sort_method = DataSorter.default_sort_report_method()
        return sorted(tickers, key=functools.cmp_to_key(sort_method))

    @staticmethod
    def default_sort_report_method():
        def default_sort_method(ticker1, ticker2):
            try:
                company_report_1 = FileStorageDAO.get_company_report(ticker1)
                company_report_2 = FileStorageDAO.get_company_report(ticker2)
            except FileNotFoundError:
                print('Did not find report for ' + ticker1 + ' or ' + ticker2 + ' when sorting.')
                return 0

            roic_list_1 = company_report_1.get(CompanyReport.RETURN_ON_INVESTED_CAPITAL)
            equity_growth_1 = company_report_1.get(CompanyReport.EQUITY_GROWTH)
            earnings_growth_1 = company_report_1.get(CompanyReport.EARNINGS_GROWTH)
            revenue_growth_1 = company_report_1.get(CompanyReport.REVENUE_GROWTH)
            operating_cash_flow_growth_1 = company_report_1.get(CompanyReport.OPERATING_CASH_GROWTH)

            roic_list_2 = company_report_2.get(CompanyReport.RETURN_ON_INVESTED_CAPITAL)
            equity_growth_2 = company_report_2.get(CompanyReport.EQUITY_GROWTH)
            earnings_growth_2 = company_report_2.get(CompanyReport.EARNINGS_GROWTH)
            revenue_growth_2 = company_report_2.get(CompanyReport.REVENUE_GROWTH)
            operating_cash_flow_growth_2 = company_report_2.get(CompanyReport.OPERATING_CASH_GROWTH)

            if len(roic_list_1) < 1 or len(equity_growth_1) < 3 or len(earnings_growth_1) < 3 or len(
                    revenue_growth_1) < 3 or len(operating_cash_flow_growth_1) < 3:
                return 0

            if len(roic_list_2) < 1 or len(equity_growth_2) < 3 or len(earnings_growth_2) < 3 or len(
                    revenue_growth_2) < 3 or len(operating_cash_flow_growth_2) < 3:
                return 0

            return roic_list_1[0] + equity_growth_1[2] + earnings_growth_1[2] + revenue_growth_1[2] + operating_cash_flow_growth_1[2] - \
                   (roic_list_2[0] + equity_growth_2[2] + earnings_growth_2[2] + revenue_growth_2[2] + operating_cash_flow_growth_2[2])
        return default_sort_method
