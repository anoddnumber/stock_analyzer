from src.scripts.financial_statement_converter import FinancialStatementConverter
from src.dao.file_storage_dao import FileStorageDAO
from src.business_objects.company_report import CompanyReport
from src.business_objects.income_statement import IncomeStatement
from src.business_objects.balance_sheet import BalanceSheet
from src.business_objects.cash_flow_statement import CashFlowStatement
from src.business_objects.key_ratios import KeyRatios
from src.business_objects.company_key_metrics_ttm import CompanyKeyMetricsTTM
from src.business_objects.company_quote import CompanyQuote
from scripts.utilities.utils import Utils
import time
import datetime
import json


class ReportGenerator:

    @staticmethod
    def generate_reports(tickers, time_to_live=0):
        for ticker in tickers:
            ReportGenerator.generate_report(ticker, time_to_live)

    @staticmethod
    def generate_report(ticker, time_to_live=0):
        try:
            info = FileStorageDAO.get_company_report(ticker)
            if time.time() - float(info.get('last_updated_date', 0)) < time_to_live:
                return
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            # continue on
            pass
        except BaseException as e:
            print("Unexpected exception when trying to generate report: " + str(e))
            return


        income_statements = FinancialStatementConverter.convert_income_statement_data(ticker)
        balance_sheets = FinancialStatementConverter.convert_balance_statement_data(ticker)
        cash_flow_statements = FinancialStatementConverter.convert_cash_flow_statement_data(ticker)
        key_ratios = FinancialStatementConverter.convert_key_ratio_data(ticker)
        company_key_metrics_ttm = FinancialStatementConverter.convert_company_key_metrics_ttm_data(ticker)
        company_quote = FinancialStatementConverter.convert_company_quote_data(ticker)

        # Part 1 - Growth rates
        equity_growth = ReportGenerator.get_growth_list(balance_sheets, BalanceSheet.SHAREHOLDERS_EQUITY)
        revenue_growth = ReportGenerator.get_growth_list(income_statements, IncomeStatement.REVENUE)
        earnings_growth = ReportGenerator.get_growth_list(income_statements, IncomeStatement.NET_INCOME)
        operating_cash_growth = ReportGenerator.get_growth_list(cash_flow_statements, CashFlowStatement.OPERATING_CASH_FLOW)

        try:
            relevant_growth_rates = [equity_growth[2], equity_growth[9],
                                     revenue_growth[2], revenue_growth[9],
                                     earnings_growth[2], earnings_growth[9],
                                     operating_cash_growth[2], operating_cash_growth[9]]

            # filter out any None values
            lowest_growth_rate = min(rate for rate in relevant_growth_rates if rate is not None)
            conservative_growth_rate = min(.15, lowest_growth_rate)
        except:
            lowest_growth_rate = 0
            conservative_growth_rate = 0

        # Part 2 - P/E and EPS
        pe_ratios = ReportGenerator.get_list(key_ratios, KeyRatios.PE_RATIO)

        positive_pe_ratios = Utils.remove_negative_numbers(pe_ratios)

        estimated_future_pe = max(min(lowest_growth_rate * 2 * 100, Utils.average(positive_pe_ratios)), 0)
        conservative_future_pe = 15

        if len(income_statements) > 0:
            eps = income_statements[0].get(IncomeStatement.EPS)
            eps_diluted = income_statements[0].get(IncomeStatement.EPS_DILUTED)
        else:
            eps = 0
            eps_diluted = 0

        if company_key_metrics_ttm is None:
            eps_ttm = 0
        else:
            eps_ttm = company_key_metrics_ttm.get(CompanyKeyMetricsTTM.EPS)

        if company_quote is None:
            shares_outstanding = 0
        else:
            shares_outstanding = company_quote.get(CompanyQuote.SHARES_OUTSTANDING)

        # Part 3 - Intrinsic value calculation
        intrinsic_value = Utils.calculate_intrinsic_value(eps, lowest_growth_rate, estimated_future_pe)
        conservative_intrinsic_value = Utils.calculate_intrinsic_value(eps_diluted, conservative_growth_rate, conservative_future_pe)

        intrinsic_value_ttm = Utils.calculate_intrinsic_value(eps_ttm, lowest_growth_rate, estimated_future_pe)
        conservative_intrinsic_value_ttm = Utils.calculate_intrinsic_value(eps_ttm, conservative_growth_rate, conservative_future_pe)

        # Part 4 - Create and populate the company report
        company_report = CompanyReport()
        company_report.set_attr(CompanyReport.DATES, ReportGenerator.get_list(income_statements, IncomeStatement.DATE))

        # Set growth rates
        company_report.set_attr(CompanyReport.EQUITY_GROWTH, equity_growth)
        company_report.set_attr(CompanyReport.REVENUE_GROWTH, revenue_growth)
        company_report.set_attr(CompanyReport.EARNINGS_GROWTH, earnings_growth)
        company_report.set_attr(CompanyReport.OPERATING_CASH_GROWTH, operating_cash_growth)

        # Debt, Revenue, Earnings, Equity, ROIC, Return on Equity, Debt to Earnings, Shares Outstanding
        company_report.set_attr(CompanyReport.RETURN_ON_INVESTED_CAPITAL, ReportGenerator.get_list(key_ratios, KeyRatios.ROIC))
        company_report.set_attr(CompanyReport.RETURN_ON_EQUITY, ReportGenerator.get_list(key_ratios, KeyRatios.ROE))
        company_report.set_attr(CompanyReport.TOTAL_DEBT, ReportGenerator.get_list(balance_sheets, BalanceSheet.TOTAL_DEBT))
        company_report.set_attr(CompanyReport.REVENUE, ReportGenerator.get_list(income_statements, IncomeStatement.REVENUE))
        company_report.set_attr(CompanyReport.EARNINGS, ReportGenerator.get_list(income_statements, IncomeStatement.NET_INCOME))
        company_report.set_attr(CompanyReport.EPS_TTM, eps_ttm)
        company_report.set_attr(CompanyReport.EQUITY, ReportGenerator.get_list(balance_sheets, BalanceSheet.SHAREHOLDERS_EQUITY))

        # other
        company_report.set_attr(CompanyReport.TICKER, ticker)
        company_report.set_attr(CompanyReport.NUM_INCOME_STATEMENTS, len(income_statements))
        company_report.set_attr(CompanyReport.NUM_BALANCE_SHEETS, len(balance_sheets))
        company_report.set_attr(CompanyReport.NUM_CASH_FLOW_STATEMENTS, len(cash_flow_statements))

        company_report.set_attr(CompanyReport.EPS, eps)
        company_report.set_attr(CompanyReport.EPS_DILUTED, eps_diluted)
        company_report.set_attr(CompanyReport.PE_RATIOS, pe_ratios)
        company_report.set_attr(CompanyReport.AVERAGE_PE_RATIO, estimated_future_pe)
        company_report.set_attr(CompanyReport.SHARES_OUTSTANDING, shares_outstanding)
        company_report.set_attr(CompanyReport.DEBT_TO_EARNINGS, ReportGenerator.get_list(key_ratios, KeyRatios.DEBT_TO_EARNINGS))

        company_report.set_attr(CompanyReport.INTRINSIC_VALUE, intrinsic_value)
        company_report.set_attr(CompanyReport.INTRINSIC_VALUE_GROWTH_RATE, lowest_growth_rate)
        company_report.set_attr(CompanyReport.CONSERVATIVE_INTRINSIC_VALUE, conservative_intrinsic_value)
        company_report.set_attr(CompanyReport.CONSERVATIVE_INTRINSIC_VALUE_GROWTH_RATE, conservative_growth_rate)

        company_report.set_attr(CompanyReport.INTRINSIC_VALUE_USING_TTM_EPS, intrinsic_value_ttm)
        company_report.set_attr(CompanyReport.CONSERVATIVE_INTRINSIC_VALUE_USING_TTM_EPS, conservative_intrinsic_value_ttm)

        FileStorageDAO.save_report(company_report)




        # Part 5 - create and save the json version of the company report
        company_report_json = {
            CompanyReport.DATES: ReportGenerator.get_list(income_statements, IncomeStatement.DATE),
            CompanyReport.EQUITY_GROWTH: equity_growth,
            CompanyReport.REVENUE_GROWTH: revenue_growth,
            CompanyReport.EARNINGS_GROWTH: earnings_growth,
            CompanyReport.OPERATING_CASH_GROWTH: operating_cash_growth,
            CompanyReport.RETURN_ON_INVESTED_CAPITAL: ReportGenerator.get_list(key_ratios, KeyRatios.ROIC),
            CompanyReport.RETURN_ON_EQUITY: ReportGenerator.get_list(key_ratios, KeyRatios.ROE),
            CompanyReport.TOTAL_DEBT: ReportGenerator.get_list(balance_sheets, BalanceSheet.TOTAL_DEBT),
            CompanyReport.REVENUE: ReportGenerator.get_list(income_statements, IncomeStatement.REVENUE),
            CompanyReport.EARNINGS: ReportGenerator.get_list(income_statements, IncomeStatement.NET_INCOME),
            CompanyReport.EPS_TTM: eps_ttm,
            CompanyReport.EQUITY: ReportGenerator.get_list(balance_sheets, BalanceSheet.SHAREHOLDERS_EQUITY),
            CompanyReport.TICKER: ticker,
            CompanyReport.NUM_INCOME_STATEMENTS: len(income_statements),
            CompanyReport.NUM_BALANCE_SHEETS: len(balance_sheets),
            CompanyReport.NUM_CASH_FLOW_STATEMENTS: len(cash_flow_statements),
            CompanyReport.EPS: eps,
            CompanyReport.EPS_DILUTED: eps_diluted,
            CompanyReport.PE_RATIOS: pe_ratios,
            CompanyReport.AVERAGE_PE_RATIO: estimated_future_pe,
            CompanyReport.SHARES_OUTSTANDING: shares_outstanding,
            CompanyReport.DEBT_TO_EARNINGS: ReportGenerator.get_list(key_ratios, KeyRatios.DEBT_TO_EARNINGS),
            CompanyReport.INTRINSIC_VALUE: intrinsic_value,
            CompanyReport.INTRINSIC_VALUE_GROWTH_RATE: lowest_growth_rate,
            CompanyReport.CONSERVATIVE_INTRINSIC_VALUE: conservative_intrinsic_value,
            CompanyReport.CONSERVATIVE_INTRINSIC_VALUE_GROWTH_RATE: conservative_growth_rate,
            CompanyReport.INTRINSIC_VALUE_USING_TTM_EPS: intrinsic_value_ttm,
            CompanyReport.CONSERVATIVE_INTRINSIC_VALUE_USING_TTM_EPS: conservative_intrinsic_value_ttm,
            'last_updated_date': time.time(),
            'last_updated_date_human': str(datetime.datetime.now())
        }

        FileStorageDAO.save_company_report_json(ticker, company_report_json)

    @staticmethod
    def get_growth(statements, num_years, attr):
        if len(statements) < num_years or len(statements) == 0:
            return 'no data'
        try:
            starting_value = float(statements[num_years].get(attr))
            ending_value = float(statements[0].get(attr))
            return Utils.calculate_yoy_return(starting_value, ending_value, num_years)
        except:
            return 'error'

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

# print(Utils.calculate_payback_time(3185, 501000000, .25, 17377000000))
# FileStorageDAO._make_directories()
# ReportGenerator.generate_report('F')
# print(Utils.calculate_intrinsic_value(34.8,.25,50))