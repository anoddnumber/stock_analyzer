from urllib.request import urlopen
import json


class FinancialModelingPrepClient:

    @staticmethod
    def get_income_statement(ticker):
        return FinancialModelingPrepClient.get_income_statements_batch([ticker])

    @staticmethod
    def get_income_statements_batch(tickers):
        if len(tickers) <= 0:
            return

        arguments = tickers[0]
        for i in range(1, len(tickers)):
            arguments += ',' + tickers[i]

        url = 'https://financialmodelingprep.com/api/v3/financials/income-statement/' + arguments
        response = urlopen(url)
        data = response.read().decode("utf-8")
        return json.loads(data)