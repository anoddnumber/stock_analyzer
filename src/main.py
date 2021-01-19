# from clients.FinancialModelingPrepClient import FinancialModelingPrepClient
from scripts.data_retriever import DataRetriever
from dao.file_storage_dao import FileStorageDAO
from scripts.data_organizer import DataOrganizer
from scripts.data_analyzer import DataAnalyzer
from scripts.data_filterer import DataFilterer
from scripts.data_sorter import DataSorter
from clients.FinancialModelingPrepClient import FinancialModelingPrepClient
from scripts.report_generator import ReportGenerator
from business_objects.company_report import CompanyReport

# ttl=60*60*24*500 # 500 days
#
# FileStorageDAO._make_directories()
# tickers = DataRetriever.retrieve_tickers(ttl)
# print('tickers: ' + str(tickers))

# ReportGenerator.generate_reports(tickers, ttl)


#
#
# def should_include(company_report):
#     roic_list = company_report.get(CompanyReport.RETURN_ON_INVESTED_CAPITAL)
#     equity_growth = company_report.get(CompanyReport.EQUITY_GROWTH)
#     earnings_growth = company_report.get(CompanyReport.EARNINGS_GROWTH)
#     revenue_growth = company_report.get(CompanyReport.REVENUE_GROWTH)
#     operating_cash_flow_growth = company_report.get(CompanyReport.OPERATING_CASH_GROWTH)
#
#     if len(roic_list) < 10 or len(equity_growth) < 10 or len(earnings_growth) < 10 or len(revenue_growth) < 10 or len(operating_cash_flow_growth) < 10:
#         return False
#
#     if roic_list[0] is None or equity_growth[2] is None or equity_growth[9] is None \
#             or earnings_growth[2] is None or earnings_growth[9] is None \
#             or revenue_growth[2] is None or revenue_growth[9] is None \
#             or operating_cash_flow_growth[2] is None or operating_cash_flow_growth[9] is None:
#         return False
#
#     return roic_list[0] > .1 \
#            and equity_growth[2] > .1 and equity_growth[9] > .1 \
#            and earnings_growth[2] > .1 and earnings_growth[9] > .1 \
#            and revenue_growth[2] > .1 and revenue_growth[9] > .1 \
#            and operating_cash_flow_growth[2] > .1 and operating_cash_flow_growth[9] > .1
#
#
#
# filtered_tickers = DataFilterer.filter_reports(tickers, should_include)
# print(filtered_tickers)



filtered_tickers = ['AMZN', 'STL', 'LULU', 'GOOGL', 'MTZ', 'HOMB', 'CBRE', 'SIVB', 'EW', 'ILMN', 'ISRG', 'EEFT', 'CSGP', 'ODFL', 'ROP', 'MLNX', 'MKTX', 'LAD', 'ANSS', 'GABC', 'MPWR', 'CACC', 'QCRH', 'IMKTA', 'INDB', 'PGC', 'HBNC', 'FMBH', 'BCBP', 'SMBC', 'MHH', 'BMTC', 'MBCN', 'TPL', 'CCNE', 'OZK', 'ATE.PA', 'MC.PA', 'DIM.PA', 'ALSER.PA', 'ADN1.DE', 'NEM.DE', 'AMZ.DE', 'ILU.DE', 'MOH.DE', 'ABEA.DE', 'BC8.DE', 'SRT.DE', 'WDI.DE', 'ABBOTINDIA.NS', 'BERGEPAINT.NS', 'IGL.NS', 'PETRONET.NS', 'AARTIDRUGS.NS', 'ALKYLAMINE.NS', 'ASTEC.NS', 'ASTRAL.NS', 'ATUL.NS', 'BHARATRAS.NS', 'DEEPAKNTR.NS', 'DELTACORP.NS', 'EXCELINDUS.NS', 'GRANULES.NS', 'HONAUT.NS', 'IOLCP.NS', 'IPCALAB.NS', 'JUBLFOOD.NS', 'KRBL.NS', 'NESCO.NS', 'SAKSOFT.NS', 'SCHAEFFLER.NS', 'SOLARINDS.NS', 'SRHHYPOLTD.NS', 'TCI.NS', 'TIMKEN.NS', 'VINATIORGA.NS', 'AHT.L', 'ASC.L', 'CRL.L', 'DOTD.L', 'FOUR.L', 'HSV.L', 'IPX.L', 'KGP.L', 'POLR.L', 'SGM.L', 'TRCN.ME', 'SIBN.ME', 'PGHN.SW', '1061.HK', '1066.HK', '1093.HK', '1099.HK', '1109.HK', '1126.HK', '1177.HK', '1313.HK', '1600.HK', '1717.HK', '1918.HK', '2020.HK', '2233.HK', '2313.HK', '2382.HK', '2688.HK', '3323.HK', '3918.HK']
sorted_tickers = DataSorter.sort_reports(filtered_tickers)
print('\n\n\nSorted tickers:\n\n')
print(sorted_tickers)

# sorted_tickers is ['NESCO.NS', 'PETRONET.NS', 'ADN1.DE', 'KGP.L', 'HSV.L', 'OZK', 'ANSS', 'HOMB', 'BMTC', 'TCI.NS', 'SOLARINDS.NS', 'SMBC', 'GABC', 'SRT.DE', 'MC.PA', 'MOH.DE', 'EEFT', 'AARTIDRUGS.NS', '1099.HK', 'ISRG', 'BERGEPAINT.NS', '1066.HK', 'ATE.PA', 'PGC', 'GOOGL', 'ABEA.DE', 'ALSER.PA', 'AHT.L', 'CCNE', 'DIM.PA', 'EW', 'MBCN', 'DOTD.L', 'CACC', '2313.HK', 'SIBN.ME', 'ROP', 'ILMN', 'ODFL', '1126.HK', 'ILU.DE', '1109.HK', 'QCRH', 'MPWR', 'IGL.NS', 'SRHHYPOLTD.NS', 'PGHN.SW', 'ATUL.NS', 'SAKSOFT.NS', '1093.HK', 'LULU', 'INDB', 'IPCALAB.NS', 'BC8.DE', 'ABBOTINDIA.NS', 'FMBH', 'HONAUT.NS', 'ASTRAL.NS', 'MKTX', '1177.HK', 'MTZ', 'LAD', 'GRANULES.NS', 'NEM.DE', 'TRCN.ME', 'DELTACORP.NS', '1600.HK', 'KRBL.NS', 'EXCELINDUS.NS', '2688.HK', 'BCBP', 'CBRE', 'ASC.L', 'TIMKEN.NS', '1061.HK', 'SCHAEFFLER.NS', 'CRL.L', 'CSGP', 'STL', 'SIVB', 'WDI.DE', 'JUBLFOOD.NS', 'VINATIORGA.NS', 'SGM.L', '2020.HK', 'FOUR.L', '3918.HK', '1313.HK', 'HBNC', 'POLR.L', 'AMZN', 'AMZ.DE', '2382.HK', 'ALKYLAMINE.NS', 'MLNX', '1717.HK', 'ASTEC.NS', 'MHH', '3323.HK', 'IPX.L', '1918.HK', 'DEEPAKNTR.NS', 'TPL', 'BHARATRAS.NS', '2233.HK', 'IOLCP.NS', 'IMKTA']


# DataRetriever.retrieve_key_ratios(tickers, ttl)
#  DataRetriever.retrieve_financial_statements(tickers, ttl)
# DataRetriever.retrieve_company_key_metrics_ttm(tickers, ttl)
# ReportGenerator.generate_reports(tickers)



# print(FinancialModelingPrepClient.get_income_statement('AAPL'))
# print(FinancialModelingPrepClient.get_income_statements_batch(['GOOG', 'AMZN']))


# DataRetriever.retrieve_income_statements(['AAPL', 'AMZN', 'GOOG'])
# DataRetriever.retrieve_income_statements(['AAPL'])


# tickers = FinancialModelingPrepClient.get_tickers()

# ttl=60*60*24*10 # 10 days
# DataRetriever.retrieve_financial_statements(tickers, ttl)

# DataRetriever.retrieve_income_statements(tickers)
# DataRetriever.retrieve_balance_sheets(tickers)
# DataRetriever.retrieve_cash_flow_statements(tickers)

# DataOrganizer.organize_ticker('AAPL', 0)
# DataOrganizer.organize_tickers(tickers, 0)
# DataAnalyzer.analyze_ticker('AAPL', 0)
# DataAnalyzer.analyze_tickers(tickers, 0)
#
#
# def get_attr(analyzed_data):
#     return analyzed_data['overall_score']
#
#
# tickers_tuple = DataFilterer.filter_greater_than(tickers, get_attr, 90)
# for info in tickers[1]:
#     print(info)

# data = DataSorter.sort(tickers_tuple[0], get_attr, reverse=True)
# for info in data:
#     print(info)

# print(FileStorageDAO.get_income_statement('AAPL'))



