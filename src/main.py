# from clients.FinancialModelingPrepClient import FinancialModelingPrepClient
from scripts.data_retriever import DataRetriever
from dao.file_storage_dao import FileStorageDAO
from scripts.data_organizer import DataOrganizer
from scripts.data_analyzer import DataAnalyzer
from scripts.data_filterer import DataFilterer
from scripts.data_sorter import DataSorter
from clients.FinancialModelingPrepClient import FinancialModelingPrepClient
from scripts.report_generator import ReportGenerator
from business_objects.company_report import CompanyReport

ttl=60*60*24*500 # 500 days

FileStorageDAO._make_directories()
tickers = DataRetriever.retrieve_tickers(ttl)
print('tickers: ' + str(tickers))

ReportGenerator.generate_reports(tickers, ttl)




def should_include(company_report):
    roic_list = company_report.get(CompanyReport.RETURN_ON_INVESTED_CAPITAL)
    equity_growth = company_report.get(CompanyReport.EQUITY_GROWTH)
    earnings_growth = company_report.get(CompanyReport.EARNINGS_GROWTH)
    revenue_growth = company_report.get(CompanyReport.REVENUE_GROWTH)
    operating_cash_flow_growth = company_report.get(CompanyReport.OPERATING_CASH_GROWTH)

    if len(roic_list) < 10 or len(equity_growth) < 10 or len(earnings_growth) < 10 or len(revenue_growth) < 10 or len(operating_cash_flow_growth) < 10:
        return False

    return roic_list[0] > .1 \
           and equity_growth[2] > .1 and equity_growth[9] > .1 \
           and earnings_growth[2] > .1 and earnings_growth[9] > .1 \
           and revenue_growth[2] > .1 and revenue_growth[9] > .1 \
           and operating_cash_flow_growth[2] > .1 and operating_cash_flow_growth[9] > .1



filtered_tickers = DataFilterer.filter_reports(tickers, should_include)
sorted_tickers = DataSorter.sort_reports(filtered_tickers)
print('\n\n\nSorted tickers:\n\n')
print(sorted_tickers)



# DataRetriever.retrieve_key_ratios(tickers, ttl)
#  DataRetriever.retrieve_financial_statements(tickers, ttl)
# DataRetriever.retrieve_company_key_metrics_ttm(tickers, ttl)
# ReportGenerator.generate_reports(tickers)



# print(FinancialModelingPrepClient.get_income_statement('AAPL'))
# print(FinancialModelingPrepClient.get_income_statements_batch(['GOOG', 'AMZN']))


# DataRetriever.retrieve_income_statements(['AAPL', 'AMZN', 'GOOG'])
# DataRetriever.retrieve_income_statements(['AAPL'])


# tickers = FinancialModelingPrepClient.get_tickers()

# ttl=60*60*24*10 # 10 days
# DataRetriever.retrieve_financial_statements(tickers, ttl)

# DataRetriever.retrieve_income_statements(tickers)
# DataRetriever.retrieve_balance_sheets(tickers)
# DataRetriever.retrieve_cash_flow_statements(tickers)

# DataOrganizer.organize_ticker('AAPL', 0)
# DataOrganizer.organize_tickers(tickers, 0)
# DataAnalyzer.analyze_ticker('AAPL', 0)
# DataAnalyzer.analyze_tickers(tickers, 0)
#
#
# def get_attr(analyzed_data):
#     return analyzed_data['overall_score']
#
#
# tickers_tuple = DataFilterer.filter_greater_than(tickers, get_attr, 90)
# for info in tickers[1]:
#     print(info)

# data = DataSorter.sort(tickers_tuple[0], get_attr, reverse=True)
# for info in data:
#     print(info)

# print(FileStorageDAO.get_income_statement('AAPL'))



