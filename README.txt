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