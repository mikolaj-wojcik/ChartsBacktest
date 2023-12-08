import pandas as pd
import yfinance as yf
import requests
import datetime
import pricesStruct
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.cryptocurrencies import CryptoCurrencies
from alpha_vantage.foreignexchange import ForeignExchange
#from alpha_vantage.timeseries
def load_csv(CSVpath = r'C:\Users\Mikolaj\Downloads\daily_IBM.csv'):
    
    data = pd.read_csv(CSVpath)

    return data #pricesStruct.generatePriceListFromDf(data)

def load_URLStock(userKey, ticker, market='', interval =0, startDate = 0, stopDate = datetime.datetime.now()):
     
    ts = TimeSeries(key= userKey,output_format= 'pandas')
    #TimeSeries.
    # Get json object with the intraday data and another with  the call's metadata
    data, meta_data = ts.get_daily(ticker, outputsize='full')
    data.reset_index(inplace=True)
    data = data.rename(columns= {'date' : 'timestamp', '2. high': 'high', '3. low': 'low','1. open': 'open','4. close': 'close'})
    
    return data
    #return pricesStruct.generatePriceListFromDf(data)