from alpha_vantage.timeseries import TimeSeries

ts = TimeSeries(key='S86TTOVAFIWT3D8B')
# Get json object with the intraday data and another with  the call's metadata
data, meta_data = ts.get_intraday('GOOGL')

print(data)