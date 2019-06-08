# from clients.FinancialModelingPrepClient import FinancialModelingPrepClient
from scripts.data_retriever import DataRetriever
from dao.file_storage_dao import FileStorageDAO
from scripts.data_organizer import DataOrganizer
from clients.FinancialModelingPrepClient import FinancialModelingPrepClient


# print(FinancialModelingPrepClient.get_income_statement('AAPL'))
# print(FinancialModelingPrepClient.get_income_statements_batch(['GOOG', 'AMZN']))


# DataRetriever.retrieve_income_statements(['AAPL', 'AMZN', 'GOOG'])


# tickers = FileStorageDAO.get_tickers()
# print('tickers')
# print(tickers)

tickers = FinancialModelingPrepClient.get_tickers()

DataRetriever.retrieve_income_statements(tickers)
# DataRetriever.retrieve_balance_sheets(tickers)
# DataRetriever.retrieve_cash_flow_statements(tickers)

# DataOrganizer.organize_ticker('AAPL', 0)
DataOrganizer.organize_tickers(tickers, 0)

# print(FileStorageDAO.get_income_statement('AAPL'))
