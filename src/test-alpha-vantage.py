from alpha_vantage.timeseries import TimeSeries
import os
import pprint
import re

ts = TimeSeries(key='S86TTOVAFIWT3D8B')
ticker = 'GOOG'
# Get json object with the intraday data and another with  the call's metadata
data, meta_data = ts.get_daily(ticker, 'full')

pp = pprint.PrettyPrinter()
data_str = pp.pformat(data).replace('\'', '"')

regex = re.compile('[0-9]\. ')
data_str = regex.sub('', data_str)

if not os.path.isdir('data'):
    os.mkdir('data')

history_file = open('data/' + ticker + '.json', 'w')
history_file.write(data_str)
history_file.close()