import pandas as pd
import yfinance as yf
import requests
import datetime
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.cryptocurrencies import CryptoCurrencies
from alpha_vantage.foreignexchange import ForeignExchange
import pricesStruct

if __name__ == "__main__":
    
    
    ts = TimeSeries(key='',output_format= 'pandas')
    # Get json object with the intraday data and another with  the call's metadata
    data = pd.read_csv(r'C:\Users\Mikolaj\Downloads\daily_IBM.csv')
    #data, meta_data = ts.get_daily('FLTR.LON')
    print(pricesStruct.generatePriceListFromDf(data))
    #print(data.dtypes)
    #print(data)
    