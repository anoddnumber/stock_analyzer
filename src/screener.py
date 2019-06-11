#!/usr/bin/env python

import sys
import os

home_dir = os.path.expanduser("~")
sys.path.append(home_dir + '/Documents/work/workspace/stock_analyzer/src')


from clients.FinancialModelingPrepClient import FinancialModelingPrepClient
from scripts.data_sorter import DataSorter
from scripts.data_organizer import DataOrganizer
from scripts.data_analyzer import DataAnalyzer
from scripts.data_filterer import DataFilterer

tickers = FinancialModelingPrepClient.get_tickers()

# DataOrganizer.organize_tickers(tickers, 0)
# DataAnalyzer.analyze_tickers(tickers, 0)


def get_attr(analyzed_data):
    return analyzed_data['overall_score']


tickers_tuple = DataFilterer.filter_greater_than(tickers, get_attr, 90)

data = DataSorter.sort(tickers_tuple[0], get_attr, reverse=True)
for info in data:
    print(info)
