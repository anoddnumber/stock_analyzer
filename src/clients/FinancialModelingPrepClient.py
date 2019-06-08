from urllib.request import urlopen
import json


class FinancialModelingPrepClient:

    @staticmethod
    def get_income_statement(ticker):
        return FinancialModelingPrepClient.get_income_statements_batch([ticker])

    @staticmethod
    def get_income_statements_batch(tickers):
        url = 'https://financialmodelingprep.com/api/v3/financials/income-statement/'
        return FinancialModelingPrepClient.json_get_financial_statement(tickers, url)

    @staticmethod
    def get_balance_sheet(ticker):
        return FinancialModelingPrepClient.get_balance_sheets_batch([ticker])

    @staticmethod
    def get_balance_sheets_batch(tickers):
        url = 'https://financialmodelingprep.com/api/v3/financials/balance-sheet-statement/'
        return FinancialModelingPrepClient.json_get_financial_statement(tickers, url)

    @staticmethod
    def get_cash_flow_sheet(ticker):
        return FinancialModelingPrepClient.get_cash_flow_sheets_batch([ticker])

    @staticmethod
    def get_cash_flow_statements_batch(tickers):
        url = 'https://financialmodelingprep.com/api/v3/financials/cash-flow-statement/'
        return FinancialModelingPrepClient.json_get_financial_statement(tickers, url)

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

    @staticmethod
    def json_get_financial_statement(tickers, url):
        if len(tickers) <= 0:
            return

        arguments = tickers[0]
        for i in range(1, len(tickers)):
            arguments += ',' + tickers[i]

        url = url + arguments
        data = FinancialModelingPrepClient.json_get(url)

        try:
            data = data['financialStatementList']
        except KeyError:
            data = [data]
        return data
