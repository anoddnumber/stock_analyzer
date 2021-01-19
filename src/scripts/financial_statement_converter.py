from src.dao.file_storage_dao import FileStorageDAO
from src.business_objects.income_statement import IncomeStatement
from src.business_objects.balance_sheet import BalanceSheet
from src.business_objects.cash_flow_statement import CashFlowStatement
from src.business_objects.key_ratios import KeyRatios
from src.business_objects.key_ratios_ttm import KeyRatiosTTM
from src.business_objects.company_key_metrics_ttm import CompanyKeyMetricsTTM
from src.business_objects.company_quote import CompanyQuote
from src.client_info.financial_modeling_prep_info import FinancialModelingPrepInfo


class FinancialStatementConverter:
    """
        Converts raw data (currently only from FinancialModelingPrep) into the corresponding business objects
    """

    @staticmethod
    def convert_income_statement_data(ticker):
        """
            Reads the raw income statement data for the given ticker and converts it into IncomeStatement objects

            :param ticker: the stock symbol
            :return: a list of income statement objects associated with the ticker that was input
        """
        json_data = FileStorageDAO.get_income_statement(ticker)

        income_statements = []
        for income_statement_data in json_data['financials']:
            income_statements.append(IncomeStatement(ticker,
                                                     FinancialModelingPrepInfo.income_statement_object_to_json_mapping,
                                                     income_statement_data))

        return income_statements

    @staticmethod
    def convert_balance_statement_data(ticker):
        """
            Reads the raw balance sheet data for the given ticker and converts it into BalanceSheet objects

            :param ticker: the stock symbol
            :return: a list of balance sheet objects associated with the ticker that was input
        """
        json_data = FileStorageDAO.get_balance_sheet(ticker)
        balance_sheets = []
        for balance_sheet_data in json_data['financials']:
            balance_sheets.append(BalanceSheet(FinancialModelingPrepInfo.balance_sheet_object_to_json_mapping,
                                               balance_sheet_data))

        return balance_sheets

    @staticmethod
    def convert_cash_flow_statement_data(ticker):
        """
            Reads the raw cash flow statement data for the given ticker and converts it into
            CashFlowStatement objects

            :param ticker: the stock symbol
            :return: a list of cash flow statement objects associated with the ticker that was input
        """
        json_data = FileStorageDAO.get_cash_flow_statement(ticker)
        cash_flow_statements = []
        for cash_flow_statement_data in json_data['financials']:
            cash_flow_statements.append(CashFlowStatement(
                FinancialModelingPrepInfo.cash_flow_statement_object_to_json_mapping, cash_flow_statement_data))

        return cash_flow_statements

    @staticmethod
    def convert_key_ratio_data(ticker):
        json_data = FileStorageDAO.get_key_ratios(ticker)
        key_ratios = []
        for key_ratio_data in json_data['financials']:
            key_ratios.append(KeyRatios(
                FinancialModelingPrepInfo.key_ratios_object_to_json_mapping, key_ratio_data))

        return key_ratios

    @staticmethod
    def convert_key_ratio_ttm_data(ticker):
        json_data = FileStorageDAO.get_key_ratios_ttm(ticker)
        return KeyRatiosTTM(FinancialModelingPrepInfo.key_ratios_ttm_object_to_json_mapping, json_data['financials'][0])

    @staticmethod
    def convert_company_key_metrics_ttm_data(ticker):
        json_data = FileStorageDAO.get_company_key_metrics_ttm(ticker)
        if len(json_data['financials']) > 0:
            return CompanyKeyMetricsTTM(FinancialModelingPrepInfo.company_key_metrics_ttm_object_to_json_mapping, json_data['financials'][0])
        # return CompanyKeyMetricsTTM(FinancialModelingPrepInfo.company_key_metrics_ttm_object_to_json_mapping, {})

    @staticmethod
    def convert_company_quote_data(ticker):
        try:
            json_data = FileStorageDAO.get_company_quote(ticker)
            return CompanyQuote(FinancialModelingPrepInfo.company_quote_object_to_json_mapping, json_data)
        except:
            return None

# print(*FinancialStatementConverter.convert_cash_flow_statement_data('AMZN'))
