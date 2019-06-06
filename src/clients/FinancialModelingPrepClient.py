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
        return FinancialModelingPrepClient.json_get(url)

    @staticmethod
    def get_tickers():
        url = 'https://financialmodelingprep.com/api/v3/company/stock/list'
        res = FinancialModelingPrepClient.json_get(url)
        tickers = []
        for datum in res['symbolsList']:
            tickers.append(datum['symbol'])
        return tickers

    @staticmethod
    def json_get(url):
        response = urlopen(url)
        data = response.read().decode("utf-8")
        return json.loads(data)

