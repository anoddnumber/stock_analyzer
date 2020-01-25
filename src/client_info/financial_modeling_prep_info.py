from business_objects.income_statement import IncomeStatement
from business_objects.balance_sheet import BalanceSheet
from business_objects.cash_flow_statement import CashFlowStatement


class FinancialModelingPrepInfo:

    income_statement_object_to_json_mapping = {
        IncomeStatement.DATE: 'date',
        IncomeStatement.REVENUE: 'Revenue',
        IncomeStatement.COST_OF_REVENUE: 'Cost of Revenue',
        IncomeStatement.GROSS_PROFIT: 'Gross Profit',
        IncomeStatement.R_AND_D_EXPENSES: 'R&D Expenses',
        IncomeStatement.S_G_AND_A_EXPENSES: 'SG&A Expense',
        IncomeStatement.OPERATING_EXPENSES: 'Operating Expenses',
        IncomeStatement.INTEREST_EXPENSES: 'Interest Expense',
        IncomeStatement.EARNINGS_BEFORE_TAX: 'Earnings before Tax',
        IncomeStatement.INCOME_TAX_EXPENSE: 'Income Tax Expense',
        IncomeStatement.NET_INCOME: 'Net Income',
        IncomeStatement.EPS: 'EPS',
        IncomeStatement.EPS_DILUTED: 'EPS Diluted',
    }

    balance_sheet_object_to_json_mapping = {
        BalanceSheet.DATE: 'date',
        BalanceSheet.CASH_AND_CASH_EQUIVALENTS: 'Cash and cash equivalents',
        BalanceSheet.ACCOUNTS_RECEIVABLE: 'Receivables',
        BalanceSheet.INTANGIBLE_ASSETS: 'Goodwill and Intangible Assets',
        BalanceSheet.NON_CURRENT_ASSETS: 'Total non-current assets',
        BalanceSheet.TOTAL_ASSETS: 'Total assets',
        BalanceSheet.ACCOUNTS_PAYABLE: 'Payables',
        BalanceSheet.CURRENT_LIABILITIES: 'Total current liabilities',
        BalanceSheet.TOTAL_DEBT: 'Total debt',
        BalanceSheet.NON_CURRENT_LIABILITIES: 'Total non-current liabilities',
        BalanceSheet.TOTAL_LIABILITIES: 'Total liabilities',
        BalanceSheet.RETAINED_EARNINGS: 'Retained earnings (deficit)',
        BalanceSheet.SHAREHOLDERS_EQUITY: 'Total shareholders equity',
    }

    cash_flow_statement_object_to_json_mapping = {
        CashFlowStatement.DATE: 'date',
        CashFlowStatement.OPERATING_CASH_FLOW: 'Operating Cash Flow',
        CashFlowStatement.CAPITAL_EXPENDITURE: 'Capital Expenditure',
        CashFlowStatement.INVESTING_CASH_FLOW: 'Investing Cash flow',
        CashFlowStatement.DEBT_REPAYMENT: 'Issuance (repayment) of debt',
        CashFlowStatement.SHARE_BUYBACK: 'Issuance (buybacks) of shares',
        CashFlowStatement.DIVIDEND_PAYMENTS: 'Dividend payments',
        CashFlowStatement.FINANCING_CASH_FLOW: 'Financing Cash Flow',
        CashFlowStatement.NET_CASH_FLOW: 'Net cash flow / Change in cash',
        CashFlowStatement.FREE_CASH_FLOW: 'Free Cash Flow',
    }