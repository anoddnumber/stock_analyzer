from urllib.request import urlopen
from scripts.utilities.utils import Utils
import json


class FinancialModelingPrepClient:

    API_KEY = Utils.get_api_key()
    INCOME_STATEMENT = 'income_statement'
    BALANCE_SHEET = 'balance_sheet'
    CASH_FLOW_STATEMENT = 'cash_flow_statement'

    @staticmethod
    def get_financial_ratios(ticker):
        url = 'https://financialmodelingprep.com/api/v3/key-metrics/' + ticker + '?apikey=' + FinancialModelingPrepClient.API_KEY
        return FinancialModelingPrepClient.json_get(url)

    @staticmethod
    def get_financial_ratios_batch(tickers):
        """
        Financial Modeling Prep doesn't have a batch API, so just loop through and use the single API
        :param tickers: stock symbols to fetch for
        :return: a list of json that contains financial ratios
        """
        ret = []
        for ticker in tickers:
            ret.append(FinancialModelingPrepClient.get_financial_ratios(ticker))
        return ret

    @staticmethod
    def get_income_statement(ticker):
        return FinancialModelingPrepClient.get_income_statements_batch([ticker])

    @staticmethod
    def get_income_statements_batch(tickers):
        return FinancialModelingPrepClient.get_batch(tickers, FinancialModelingPrepClient.INCOME_STATEMENT)

    @staticmethod
    def get_balance_sheet(ticker):
        return FinancialModelingPrepClient.get_balance_sheets_batch([ticker])

    @staticmethod
    def get_balance_sheets_batch(tickers):
        return FinancialModelingPrepClient.get_batch(tickers, FinancialModelingPrepClient.BALANCE_SHEET)

    @staticmethod
    def get_batch(tickers, statement_type):
        # TODO: See if the batch API is fixed..
        ret = []
        for ticker in tickers:
            # time.sleep(1)
            ret.append(FinancialModelingPrepClient.json_get_single_financial_statement(ticker, statement_type))
        return ret

    @staticmethod
    def get_cash_flow_sheet(ticker):
        return FinancialModelingPrepClient.get_cash_flow_sheets_batch([ticker])

    @staticmethod
    def get_cash_flow_statements_batch(tickers):
        return FinancialModelingPrepClient.get_batch(tickers, FinancialModelingPrepClient.CASH_FLOW_STATEMENT)

    @staticmethod
    def get_tickers():
        url = 'https://financialmodelingprep.com/api/v3/company/stock/list' + '?apikey=' + FinancialModelingPrepClient.API_KEY
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
    def json_get_single_financial_statement(ticker, statement_type):
        if statement_type == 'income_statement':
            url = 'https://financialmodelingprep.com/api/v3/income-statement/'
        elif statement_type == FinancialModelingPrepClient.BALANCE_SHEET:
            url = 'https://financialmodelingprep.com/api/v3/balance-sheet-statement/'
        elif statement_type == 'cash_flow_statement':
            url = 'https://financialmodelingprep.com/api/v3/cash-flow-statement/'

        url = url + ticker + '?apikey=' + FinancialModelingPrepClient.API_KEY
        data = FinancialModelingPrepClient.json_get(url)

        return data

    @staticmethod
    def json_get_financial_statement(tickers, url):
        if len(tickers) <= 0:
            return

        arguments = tickers[len(tickers) - 1]
        for i in range(len(tickers) - 2, -1, -1):
            arguments += ',' + tickers[i]

        url = url + arguments + '?apikey=' + FinancialModelingPrepClient.API_KEY
        print('url ' + url)
        data = FinancialModelingPrepClient.json_get(url)

        try:
            data = data['financialStatementList']
        except KeyError:
            data = [data]
        return data
