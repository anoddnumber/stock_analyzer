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
    def generate_reports(tickers):
        for ticker in tickers:
            ReportGenerator.generate_report(ticker)

    @staticmethod
    def generate_report(ticker):
        income_statements = FinancialStatementConverter.convert_income_statement_data(ticker)
        balance_sheets = FinancialStatementConverter.convert_balance_statement_data(ticker)
        cash_flow_statements = FinancialStatementConverter.convert_cash_flow_statement_data(ticker)

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


        lowest_growth_rate = min(revenue_growth_3_year, revenue_growth_10_year, earnings_growth_3_year,
                                 earnings_growth_10_year, equity_growth_3_year, equity_growth_10_year,
                                 operating_cash_growth_3_year, operating_cash_growth_10_year)
        conservative_growth_rate = min(.15, lowest_growth_rate)

        # TODO calculate a suitable P/E ratio
        intrinsic_value = Utils.calculate_intrinsic_value(IncomeStatement.EPS, lowest_growth_rate, 15)
        conservative_intrinsic_value = Utils.calculate_intrinsic_value(IncomeStatement.EPS_DILUTED, conservative_growth_rate, 15)

        # Create and populate the company report
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

        # Debt, Revenue, Earnings, Equity, ROIC, Return on Equity, Debt to Earnings, Shares Outstanding
        company_report.set_attr(CompanyReport.TOTAL_DEBT_0_YEAR,
                                ReportGenerator.get_value(balance_sheets, 0, BalanceSheet.TOTAL_DEBT))
        company_report.set_attr(CompanyReport.TOTAL_DEBT_3_YEAR,
                                ReportGenerator.get_value(balance_sheets, 3, BalanceSheet.TOTAL_DEBT))
        company_report.set_attr(CompanyReport.TOTAL_DEBT_5_YEAR,
                                ReportGenerator.get_value(balance_sheets, 5, BalanceSheet.TOTAL_DEBT))
        company_report.set_attr(CompanyReport.TOTAL_DEBT_10_YEAR,
                                ReportGenerator.get_value(balance_sheets, 10, BalanceSheet.TOTAL_DEBT))

        company_report.set_attr(CompanyReport.REVENUE_0_YEAR,
                                ReportGenerator.get_value(income_statements, 0, IncomeStatement.REVENUE))
        company_report.set_attr(CompanyReport.REVENUE_3_YEAR,
                                ReportGenerator.get_value(income_statements, 3, IncomeStatement.REVENUE))
        company_report.set_attr(CompanyReport.REVENUE_5_YEAR,
                                ReportGenerator.get_value(income_statements, 5, IncomeStatement.REVENUE))
        company_report.set_attr(CompanyReport.REVENUE_10_YEAR,
                                ReportGenerator.get_value(income_statements, 10, IncomeStatement.REVENUE))

        company_report.set_attr(CompanyReport.EARNINGS_0_YEAR,
                                ReportGenerator.get_value(income_statements, 0, IncomeStatement.NET_INCOME))
        company_report.set_attr(CompanyReport.EARNINGS_3_YEAR,
                                ReportGenerator.get_value(income_statements, 3, IncomeStatement.NET_INCOME))
        company_report.set_attr(CompanyReport.EARNINGS_5_YEAR,
                                ReportGenerator.get_value(income_statements, 5, IncomeStatement.NET_INCOME))
        company_report.set_attr(CompanyReport.EARNINGS_10_YEAR,
                                ReportGenerator.get_value(income_statements, 10, IncomeStatement.NET_INCOME))

        company_report.set_attr(CompanyReport.EQUITY_0_YEAR,
                                ReportGenerator.get_value(income_statements, 0, BalanceSheet.SHAREHOLDERS_EQUITY))
        company_report.set_attr(CompanyReport.EQUITY_3_YEAR,
                                ReportGenerator.get_value(income_statements, 3, BalanceSheet.SHAREHOLDERS_EQUITY))
        company_report.set_attr(CompanyReport.EQUITY_5_YEAR,
                                ReportGenerator.get_value(income_statements, 5, BalanceSheet.SHAREHOLDERS_EQUITY))
        company_report.set_attr(CompanyReport.EQUITY_10_YEAR,
                                ReportGenerator.get_value(income_statements, 10, BalanceSheet.SHAREHOLDERS_EQUITY))

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

        company_report.set_attr(CompanyReport.EPS, IncomeStatement.EPS)
        company_report.set_attr(CompanyReport.EPS_DILUTED, IncomeStatement.EPS_DILUTED)

        company_report.set_attr(CompanyReport.INTRINSIC_VALUE, intrinsic_value)
        company_report.set_attr(CompanyReport.CONSERVATE_INTRINSIC_VALUE, conservative_intrinsic_value)

        FileStorageDAO.save_report(company_report)

    @staticmethod
    def get_growth(statements, num_years, attr):
        if len(statements) < num_years:
            return 'no data'
        starting_value = float(statements[num_years].get(attr))
        ending_value = float(statements[0].get(attr))
        return Utils.calculate_yoy_return(starting_value, ending_value, num_years)

    @staticmethod
    def get_value(statements, num_years, attr):
        if len(statements) < num_years:
            return 'no data'
        return float(statements[num_years].get(attr))

# DataRetriever.retrieve_income_statements(['AAPL', 'AMZN', 'GOOG'])
# all_tickers = FinancialModelingPrepClient.get_tickers()
# print(all_tickers)
# print(len(all_tickers))
# DataRetriever.retrieve_financial_statements(['AMZN'], 60 * 60 * 24 * 10)
# DataRetriever.retrieve_financial_statements(all_tickers, 60 * 60 * 24 * 10)
# ReportGenerator.generate_report(all_tickers)

# ReportGenerator.generate_report('AAPL')
