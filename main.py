import pandas as pd
import yfinance as yf
import requests
import datetime
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.cryptocurrencies import CryptoCurrencies
from alpha_vantage.foreignexchange import ForeignExchange
import loadData
import Strategies.SMAcross as Strat
import RunStrategy as Run

if __name__ == "__main__":
    # Get json object with the intraday data and another with  the call's metadata
   # data = pd.read_csv(r'C:\Users\Mikolaj\Downloads\daily_IBM.csv')
    #data = pd.read_csv(r'frame.csv')
    prices = loadData.load_URLStock('670VPCC632C40KBM', 'DOW')
    start = Run.RunStrategy(prices, Strat.SMAcross())
    start.runStrategy()
    #print(data.dtypes)
    #print(data)
    