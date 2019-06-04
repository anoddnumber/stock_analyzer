# from clients.FinancialModelingPrepClient import FinancialModelingPrepClient
from scripts.data_retriever import DataRetriever


# print(FinancialModelingPrepClient.get_income_statement('AAPL'))
# print(FinancialModelingPrepClient.get_income_statements_batch(['GOOG', 'AMZN']))


DataRetriever.retrieve_income_statements(['AMZN'])