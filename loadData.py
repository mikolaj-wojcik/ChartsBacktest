import pandas as pd
import yfinance as yf
import requests
import datetime
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.cryptocurrencies import CryptoCurrencies
from alpha_vantage.foreignexchange import ForeignExchange
#from alpha_vantage.timeseries
if __name__ == "__main__":
    
    
    ts = TimeSeries(key='DUPFPREOFAYK1HDI',output_format= 'pandas')
    # Get json object with the intraday data and another with  the call's metadata
    data, meta_data = ts.get_intraday('GOOGL')
    print(data.dtypes)
    print(data)


def loadData(userKey, ticker, market, interval, startDate, stopDate = datetime.datetime.now()):
     
    ts = TimeSeries(key= userKey,output_format= 'pandas')
    #TimeSeries.
    # Get json object with the intraday data and another with  the call's metadata
    data, meta_data = ts.get_intraday('TSCO.LON')
    print(data.dtypes)
    print(data)