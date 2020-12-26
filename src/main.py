# from clients.FinancialModelingPrepClient import FinancialModelingPrepClient
from scripts.data_retriever import DataRetriever
from dao.file_storage_dao import FileStorageDAO
from scripts.data_organizer import DataOrganizer
from scripts.data_analyzer import DataAnalyzer
from scripts.data_filterer import DataFilterer
from scripts.data_sorter import DataSorter
from clients.FinancialModelingPrepClient import FinancialModelingPrepClient
from scripts.report_generator import ReportGenerator

FileStorageDAO._make_directories()
tickers = FinancialModelingPrepClient.get_tickers()
print('tickers: ' + str(tickers))
DataRetriever.retrieve_all(tickers)
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



