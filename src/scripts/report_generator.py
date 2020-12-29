from src.scripts.financial_statement_converter import FinancialStatementConverter
from src.dao.file_storage_dao import FileStorageDAO
from src.business_objects.company_report import CompanyReport
from src.business_objects.income_statement import IncomeStatement
from src.business_objects.balance_sheet import BalanceSheet
from src.business_objects.cash_flow_statement import CashFlowStatement
from scripts.utilities.utils import Utils


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

        equity_growth = ReportGenerator.get_growth_list(balance_sheets, BalanceSheet.SHAREHOLDERS_EQUITY)
        revenue_growth = ReportGenerator.get_growth_list(income_statements, IncomeStatement.REVENUE)
        earnings_growth = ReportGenerator.get_growth_list(income_statements, IncomeStatement.NET_INCOME)
        operating_cash_growth = ReportGenerator.get_growth_list(cash_flow_statements, CashFlowStatement.OPERATING_CASH_FLOW)

        revenue_growth_3_year = ReportGenerator.get_growth(income_statements, 3, IncomeStatement.REVENUE)
        revenue_growth_10_year = ReportGenerator.get_growth(income_statements, 10, IncomeStatement.REVENUE)

        earnings_growth_3_year = ReportGenerator.get_growth(income_statements, 3, IncomeStatement.NET_INCOME)
        earnings_growth_10_year = ReportGenerator.get_growth(income_statements, 10, IncomeStatement.NET_INCOME)

        equity_growth_3_year = ReportGenerator.get_growth(balance_sheets, 3, BalanceSheet.SHAREHOLDERS_EQUITY)
        equity_growth_10_year = ReportGenerator.get_growth(balance_sheets, 10, BalanceSheet.SHAREHOLDERS_EQUITY)

        operating_cash_growth_3_year = ReportGenerator.get_growth(cash_flow_statements, 3,
                                                                  CashFlowStatement.OPERATING_CASH_FLOW)
        operating_cash_growth_10_year = ReportGenerator.get_growth(cash_flow_statements, 10,
                                                                   CashFlowStatement.OPERATING_CASH_FLOW)

        lowest_growth_rate = min(revenue_growth_3_year, revenue_growth_10_year, earnings_growth_3_year,
                                 earnings_growth_10_year, equity_growth_3_year, equity_growth_10_year,
                                 operating_cash_growth_3_year, operating_cash_growth_10_year)
        conservative_growth_rate = min(.15, lowest_growth_rate)

        # TODO calculate a suitable P/E ratio

        eps = income_statements[0].get(IncomeStatement.EPS)
        eps_diluted = income_statements[0].get(IncomeStatement.EPS_DILUTED)

        intrinsic_value = Utils.calculate_intrinsic_value(eps, lowest_growth_rate, 15)
        conservative_intrinsic_value = Utils.calculate_intrinsic_value(eps_diluted, conservative_growth_rate, 15)

        # Create and populate the company report
        company_report = CompanyReport()

        # Set growth rates
        company_report.set_attr(CompanyReport.EQUITY_GROWTH, equity_growth)
        company_report.set_attr(CompanyReport.REVENUE_GROWTH, revenue_growth)
        company_report.set_attr(CompanyReport.EARNINGS_GROWTH, earnings_growth)
        company_report.set_attr(CompanyReport.OPERATING_CASH_GROWTH, operating_cash_growth)

        # Debt, Revenue, Earnings, Equity, ROIC, Return on Equity, Debt to Earnings, Shares Outstanding
        company_report.set_attr(CompanyReport.TOTAL_DEBT, ReportGenerator.get_list(balance_sheets, BalanceSheet.TOTAL_DEBT))
        company_report.set_attr(CompanyReport.REVENUE, ReportGenerator.get_list(income_statements, IncomeStatement.REVENUE))
        company_report.set_attr(CompanyReport.EARNINGS, ReportGenerator.get_list(income_statements, IncomeStatement.REVENUE))
        company_report.set_attr(CompanyReport.EQUITY, ReportGenerator.get_list(balance_sheets, BalanceSheet.SHAREHOLDERS_EQUITY))

        # other

        company_report.set_attr(CompanyReport.TICKER, ticker)
        company_report.set_attr(CompanyReport.NUM_INCOME_STATEMENTS, len(income_statements))
        company_report.set_attr(CompanyReport.NUM_BALANCE_SHEETS, len(balance_sheets))
        company_report.set_attr(CompanyReport.NUM_CASH_FLOW_STATEMENTS, len(cash_flow_statements))

        company_report.set_attr(CompanyReport.EPS, income_statements[0].get(IncomeStatement.EPS))
        company_report.set_attr(CompanyReport.EPS_DILUTED, income_statements[0].get(IncomeStatement.EPS_DILUTED))

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

    @staticmethod
    def get_list(statements, attr):
        """
        :param statements: a list of financial statements
        :param attr: the attribute you want
        :return: a list containing all the values of that particular attribute
        """
        ret = []
        for i in range(len(statements)):
            ret.append(statements[i].get(attr))
        return ret

    @staticmethod
    def get_growth_list(statements, attr):
        ret = []

        # start from 1 since growth requires more than 0 years
        for i in range(1, len(statements)):
            ret.append(ReportGenerator.get_growth(statements, i, attr))
        return ret

ReportGenerator.generate_report('AMZN')
