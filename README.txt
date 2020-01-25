This project will do several things.

1) Download historical and current stock data
2) Download historical and current financial documents' data (Income Statement, Balance Sheet, and Cashflow Statement)
3) Have utilities to calculate intrinsic value of a stock and other indicators
4) Have a UI to display the data
5) Have a way to sort and filter the data by certain characteristics
6) Have a way to simulate buying and selling securities from the past with fake money

Some things to think about:
- How should we store the stock data?
- We will want APIs to sort and filter the data, so we should store the data in a way that is easy to do so.
- How to hide/retrieve the API key?
- We may have multiple sources in the future, how do model that and make it fit in the flow?


To download historical data, we can use Alpha Vantage's free APIs (https://www.alphavantage.co/).
There is a wrapper for the APIs over here: https://github.com/RomelTorres/alpha_vantage


To install dependencies on your local computer, use virtual env (https://virtualenv.pypa.io/en/stable/installation/)

Run the following to create a virtual environment called 'env':

    virtualenv env

Run the following to activate the virtual environment:

    source env/bin/activate

Run the following to deactivate the virtual environment:

    deactivate

Install the Alpha Vantage wrapper:

    pip install alpha_vantage

How should we store the stock data?
- For now, we can create a file for each ticker, containing the ending price of the stock on a daily level. This will make it easy to retrieve a stock's price history.
- We can also store the stock prices based on date. This will make it easy to sort or get a snapshot of prices on a particular date.
- We will want to consider saving the data in a database instead of text files later and to also have a cache.

How are we going to get Financial Statement data?
- Possibly from FinancialModelingPrep (https://financialmodelingprep.com/developer/docs) - this only gives information for the last 5 years. We also would want quarterly information
- Possibly from MorningStar: https://gist.github.com/hahnicity/45323026693cdde6a116

How can we get the list of available stock tickers? How about historical stock tickers?
- Possibly from NASDAQ: https://www.nasdaq.com/screening/companies-by-industry.aspx?exchange=NASDAQ
- Possibly better than above: https://quant.stackexchange.com/questions/1640/where-to-download-list-of-all-common-stocks-traded-on-nyse-nasdaq-and-amex


Stock Analyzer will have the following steps:
1) Get raw data from sources
2) Translate the raw sources into the Income Statement, Balance Sheet, and Cash Flow Statement business objects. This step may involve a different translator for each source.
3) Create a report using the Income Statement, Balance Sheet, and Cash Flow Statement for each company. Save the reports to disk (each stock is a separate file).
4) Sort, filter, and search on the files.

There will be several different scripts required to do this:
1) Script to download the raw data and store them in files.
2) Script to convert the raw data into business objects
3) Scripts to sort, filter, and search
4) Scripts to do steps 1 and 2 automatically.