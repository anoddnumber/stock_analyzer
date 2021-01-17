from business_objects.income_statement import IncomeStatement
from business_objects.balance_sheet import BalanceSheet
from business_objects.cash_flow_statement import CashFlowStatement
from business_objects.key_ratios import KeyRatios
from business_objects.company_quote import CompanyQuote


class FinancialModelingPrepInfo:

    # the key represents the property in the income statement object
    # the value represents what the object that contains the data calls it
    income_statement_object_to_json_mapping = {
        IncomeStatement.DATE: 'date',
        IncomeStatement.REVENUE: 'revenue',
        IncomeStatement.COST_OF_REVENUE: 'costOfRevenue',
        IncomeStatement.GROSS_PROFIT: 'grossProfit',
        IncomeStatement.R_AND_D_EXPENSES: 'researchAndDevelopmentExpenses',
        IncomeStatement.S_G_AND_A_EXPENSES: 'generalAndAdministrativeExpenses',
        IncomeStatement.OPERATING_EXPENSES: 'operatingExpenses',
        IncomeStatement.INTEREST_EXPENSES: 'interestExpense',
        IncomeStatement.EARNINGS_BEFORE_TAX: 'incomeBeforeTax',
        IncomeStatement.INCOME_TAX_EXPENSE: 'incomeTaxExpense',
        IncomeStatement.NET_INCOME: 'netIncome',
        IncomeStatement.EPS: 'eps',
        IncomeStatement.EPS_DILUTED: 'epsdiluted',
    }

    balance_sheet_object_to_json_mapping = {
        BalanceSheet.DATE: 'date',
        BalanceSheet.CASH_AND_CASH_EQUIVALENTS: 'cashAndCashEquivalents',
        BalanceSheet.INTANGIBLE_ASSETS: 'goodwillAndIntangibleAssets',
        BalanceSheet.CURRENT_ASSETS: 'totalCurrentAssets',
        BalanceSheet.NON_CURRENT_ASSETS: 'totalNonCurrentAssets',
        BalanceSheet.TOTAL_ASSETS: 'totalAssets',
        BalanceSheet.ACCOUNTS_PAYABLE: 'accountPayables',
        BalanceSheet.CURRENT_LIABILITIES: 'totalCurrentLiabilities',
        BalanceSheet.TOTAL_DEBT: 'totalDebt',
        BalanceSheet.NON_CURRENT_LIABILITIES: 'totalNonCurrentLiabilities',
        BalanceSheet.TOTAL_LIABILITIES: 'totalLiabilities',
        BalanceSheet.RETAINED_EARNINGS: 'retainedEarnings',
        BalanceSheet.SHAREHOLDERS_EQUITY: 'totalStockholdersEquity',
        BalanceSheet.FIXED_ASSETS: 'propertyPlantEquipmentNet',
        BalanceSheet.INVENTORY: 'inventory',
    }

    cash_flow_statement_object_to_json_mapping = {
        CashFlowStatement.DATE: 'date',
        CashFlowStatement.OPERATING_CASH_FLOW: 'operatingCashFlow',
        CashFlowStatement.CAPITAL_EXPENDITURE: 'capitalExpenditure',
        CashFlowStatement.INVESTING_CASH_FLOW: 'netCashUsedForInvestingActivites',
        CashFlowStatement.DEBT_REPAYMENT: 'debtRepayment',
        CashFlowStatement.SHARE_BUYBACK: 'commonStockRepurchased',
        CashFlowStatement.DIVIDEND_PAYMENTS: 'dividendsPaid',
        CashFlowStatement.FINANCING_CASH_FLOW: 'netCashUsedProvidedByFinancingActivities',
        CashFlowStatement.NET_CASH_FLOW: 'netChangeInCash',
        CashFlowStatement.FREE_CASH_FLOW: 'freeCashFlow',
    }

    key_ratios_object_to_json_mapping = {
        KeyRatios.DATE: 'date',
        KeyRatios.PE_RATIO: 'peRatio',
        KeyRatios.DEBT_TO_EARNINGS: 'netDebtToEBITDA',
        KeyRatios.ROIC: 'roic',
        KeyRatios.ROE: 'roe'
    }

    company_quote_object_to_json_mapping = {
        CompanyQuote.SHARES_OUTSTANDING: 'sharesOutstanding'
    }