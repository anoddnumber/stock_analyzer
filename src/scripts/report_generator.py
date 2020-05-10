from src.scripts.financial_statement_converter import FinancialStatementConverter
from src.dao.file_storage_dao import FileStorageDAO
from src.business_objects.company_report import CompanyReport
from src.business_objects.income_statement import IncomeStatement
from src.business_objects.balance_sheet import BalanceSheet
from scripts.data_retriever import DataRetriever


class ReportGenerator:

    @staticmethod
    def generate_report(ticker):
        income_statements = FinancialStatementConverter.convert_income_statement_data(ticker)
        balance_sheets = FinancialStatementConverter.convert_balance_statement_data(ticker)
        cash_flow_statements = FinancialStatementConverter.convert_cash_flow_statement_data(ticker)

        print(income_statements[0])

        gross_profit = float(getattr(income_statements[0], IncomeStatement.GROSS_PROFIT, 'no gross profit'))
        operating_expenses = float(getattr(income_statements[0], IncomeStatement.OPERATING_EXPENSES, 'no operating expenses'))
        tax_expense = float(getattr(income_statements[0], IncomeStatement.INCOME_TAX_EXPENSE, 'no income tax expense'))
        shareholders_equity = float(getattr(balance_sheets[0], BalanceSheet.SHAREHOLDERS_EQUITY, 'no shareholder equity'))
        debt = float(getattr(balance_sheets[0], BalanceSheet.TOTAL_DEBT, 'no total debt'))

        # net operating profit after tax
        nopat_1_year = gross_profit - operating_expenses - tax_expense
        financing_1_year = shareholders_equity + debt

        roic_1_year = nopat_1_year / financing_1_year

        # print('gross profit: ' + str(gross_profit))
        # print('nopat: ' + str(nopat_1_year))
        # print('financing: ' + str(financing_1_year))
        # print('roic: ' + str(roic_1_year))

        company_report = CompanyReport()

        company_report.set_attr(CompanyReport.TICKER, ticker)
        # company_report.set_attr(CompanyReport.EQUITY_GROWTH, )
        company_report.set_attr(CompanyReport.NUM_INCOME_STATEMENTS, len(income_statements))
        company_report.set_attr(CompanyReport.NUM_BALANCE_SHEETS, len(balance_sheets))
        company_report.set_attr(CompanyReport.NUM_CASH_FLOW_STATEMENTS, len(cash_flow_statements))
        company_report.set_attr(CompanyReport.RETURN_ON_INVESTED_CAPITAL_1_YEAR, roic_1_year)

        FileStorageDAO.save_report(company_report)


# DataRetriever.retrieve_income_statements(['AAPL', 'AMZN', 'GOOG'])
ReportGenerator.generate_report('AMZN')