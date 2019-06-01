from clients.FinancialModelingPrepClient import FinancialModelingPrepClient

# print(FinancialModelingPrepClient.get_income_statement('AAPL'))
print(FinancialModelingPrepClient.get_income_statements_batch(['GOOG', 'AMZN']))