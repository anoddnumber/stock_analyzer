from src.scripts.financial_statement_converter import FinancialStatementConverter
from src.dao.file_storage_dao import FileStorageDAO
from src.business_objects.company_report import CompanyReport
from src.business_objects.income_statement import IncomeStatement
from src.business_objects.balance_sheet import BalanceSheet
from src.business_objects.cash_flow_statement import CashFlowStatement
from scripts.data_retriever import DataRetriever
from scripts.utilities.utils import Utils
from src.clients.FinancialModelingPrepClient import FinancialModelingPrepClient


class ReportGenerator:

    @staticmethod
    def generate_report(ticker):
        income_statements = FinancialStatementConverter.convert_income_statement_data(ticker)
        balance_sheets = FinancialStatementConverter.convert_balance_statement_data(ticker)
        cash_flow_statements = FinancialStatementConverter.convert_cash_flow_statement_data(ticker)

        # print(income_statements[0])

        gross_profit = float(getattr(income_statements[0], IncomeStatement.GROSS_PROFIT, 'no gross profit'))
        operating_expenses = float(getattr(income_statements[0], IncomeStatement.OPERATING_EXPENSES, 'no operating expenses'))
        tax_expense = float(getattr(income_statements[0], IncomeStatement.INCOME_TAX_EXPENSE, 'no income tax expense'))
        shareholders_equity = float(getattr(balance_sheets[0], BalanceSheet.SHAREHOLDERS_EQUITY, 'no shareholder equity'))
        debt = float(getattr(balance_sheets[0], BalanceSheet.TOTAL_DEBT, 'no total debt'))

        # net operating profit after tax
        nopat_1_year = gross_profit - operating_expenses - tax_expense
        financing_1_year = shareholders_equity + debt

        # return on invested capital
        roic_1_year = nopat_1_year / financing_1_year

        # print('gross profit: ' + str(gross_profit))
        # print('nopat: ' + str(nopat_1_year))
        # print('financing: ' + str(financing_1_year))
        # print('roic: ' + str(roic_1_year))



        # Part 1 - Growth rates

        revenue_growth_1_year = ReportGenerator.get_growth(income_statements, 1, IncomeStatement.REVENUE)
        revenue_growth_3_year = ReportGenerator.get_growth(income_statements, 3, IncomeStatement.REVENUE)
        revenue_growth_5_year = ReportGenerator.get_growth(income_statements, 5, IncomeStatement.REVENUE)
        revenue_growth_10_year = ReportGenerator.get_growth(income_statements, 10, IncomeStatement.REVENUE)

        earnings_growth_1_year = ReportGenerator.get_growth(income_statements, 1, IncomeStatement.NET_INCOME)
        earnings_growth_3_year = ReportGenerator.get_growth(income_statements, 3, IncomeStatement.NET_INCOME)
        earnings_growth_5_year = ReportGenerator.get_growth(income_statements, 5, IncomeStatement.NET_INCOME)
        earnings_growth_10_year = ReportGenerator.get_growth(income_statements, 10, IncomeStatement.NET_INCOME)

        equity_growth_1_year = ReportGenerator.get_growth(balance_sheets, 1, BalanceSheet.SHAREHOLDERS_EQUITY)
        equity_growth_3_year = ReportGenerator.get_growth(balance_sheets, 3, BalanceSheet.SHAREHOLDERS_EQUITY)
        equity_growth_5_year = ReportGenerator.get_growth(balance_sheets, 5, BalanceSheet.SHAREHOLDERS_EQUITY)
        equity_growth_10_year = ReportGenerator.get_growth(balance_sheets, 10, BalanceSheet.SHAREHOLDERS_EQUITY)

        operating_cash_growth_1_year = ReportGenerator.get_growth(cash_flow_statements, 1,
                                                                  CashFlowStatement.OPERATING_CASH_FLOW)
        operating_cash_growth_3_year = ReportGenerator.get_growth(cash_flow_statements, 3,
                                                                  CashFlowStatement.OPERATING_CASH_FLOW)
        operating_cash_growth_5_year = ReportGenerator.get_growth(cash_flow_statements, 5,
                                                                  CashFlowStatement.OPERATING_CASH_FLOW)
        operating_cash_growth_10_year = ReportGenerator.get_growth(cash_flow_statements, 10,
                                                                   CashFlowStatement.OPERATING_CASH_FLOW)


        full_equity_growth = ReportGenerator.get_growth(balance_sheets, len(balance_sheets) - 1,
                                                        BalanceSheet.SHAREHOLDERS_EQUITY)
        full_earnings_growth = ReportGenerator.get_growth(income_statements, len(income_statements) - 1,
                                                          IncomeStatement.NET_INCOME)
        full_revenue_growth = ReportGenerator.get_growth(income_statements, len(income_statements) - 1,
                                                         IncomeStatement.REVENUE)
        full_cash_growth = ReportGenerator.get_growth(balance_sheets, len(balance_sheets) - 1,
                                                      BalanceSheet.CASH_AND_CASH_EQUIVALENTS)

        company_report = CompanyReport()


        # Set growth rates
        company_report.set_attr(CompanyReport.REVENUE_GROWTH_1_YEAR, revenue_growth_1_year)
        company_report.set_attr(CompanyReport.REVENUE_GROWTH_3_YEAR, revenue_growth_3_year)
        company_report.set_attr(CompanyReport.REVENUE_GROWTH_5_YEAR, revenue_growth_5_year)
        company_report.set_attr(CompanyReport.REVENUE_GROWTH_10_YEAR, revenue_growth_10_year)

        company_report.set_attr(CompanyReport.EARNINGS_GROWTH_1_YEAR, earnings_growth_1_year)
        company_report.set_attr(CompanyReport.EARNINGS_GROWTH_3_YEAR, earnings_growth_3_year)
        company_report.set_attr(CompanyReport.EARNINGS_GROWTH_5_YEAR, earnings_growth_5_year)
        company_report.set_attr(CompanyReport.EARNINGS_GROWTH_10_YEAR, earnings_growth_10_year)

        company_report.set_attr(CompanyReport.EQUITY_GROWTH_1_YEAR, equity_growth_1_year)
        company_report.set_attr(CompanyReport.EQUITY_GROWTH_3_YEAR, equity_growth_3_year)
        company_report.set_attr(CompanyReport.EQUITY_GROWTH_5_YEAR, equity_growth_5_year)
        company_report.set_attr(CompanyReport.EQUITY_GROWTH_10_YEAR, equity_growth_10_year)

        company_report.set_attr(CompanyReport.OPERATING_CASH_GROWTH_1_YEAR, operating_cash_growth_1_year)
        company_report.set_attr(CompanyReport.OPERATING_CASH_GROWTH_3_YEAR, operating_cash_growth_3_year)
        company_report.set_attr(CompanyReport.OPERATING_CASH_GROWTH_5_YEAR, operating_cash_growth_5_year)
        company_report.set_attr(CompanyReport.OPERATING_CASH_GROWTH_10_YEAR, operating_cash_growth_10_year)

        # other

        company_report.set_attr(CompanyReport.TICKER, ticker)
        company_report.set_attr(CompanyReport.NUM_INCOME_STATEMENTS, len(income_statements))
        company_report.set_attr(CompanyReport.NUM_BALANCE_SHEETS, len(balance_sheets))
        company_report.set_attr(CompanyReport.NUM_CASH_FLOW_STATEMENTS, len(cash_flow_statements))
        company_report.set_attr(CompanyReport.RETURN_ON_INVESTED_CAPITAL_1_YEAR, roic_1_year)
        company_report.set_attr(CompanyReport.EQUITY_GROWTH, full_equity_growth)
        company_report.set_attr(CompanyReport.EARNINGS_GROWTH, full_earnings_growth)
        company_report.set_attr(CompanyReport.REVENUE_GROWTH, full_revenue_growth)
        company_report.set_attr(CompanyReport.CASH_GROWTH, full_cash_growth)

        FileStorageDAO.save_report(company_report)

    @staticmethod
    def get_growth(statements, num_years, attr):
        if len(statements) < num_years:
            return 'no data'
        starting_value = float(statements[num_years].get(attr))
        ending_value = float(statements[0].get(attr))
        return Utils.calculate_yoy_return(starting_value, ending_value, num_years)


# DataRetriever.retrieve_income_statements(['AAPL', 'AMZN', 'GOOG'])
# all_tickers = FinancialModelingPrepClient.get_tickers()
# print(all_tickers)
# print(len(all_tickers))
# DataRetriever.retrieve_financial_statements(['AMZN'], 60 * 60 * 24 * 10)
# DataRetriever.retrieve_financial_statements(all_tickers, 60 * 60 * 24 * 10)
# ReportGenerator.generate_report(all_tickers)

ReportGenerator.generate_report('AAPL')
