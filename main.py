import pandas as pd
import yfinance as yf
import requests
import datetime
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.cryptocurrencies import CryptoCurrencies
from alpha_vantage.foreignexchange import ForeignExchange
import loadData
import Strategies.SMAcross as Strat
import RunStrategy.RunStrategy as Run
from RunStrategy.StartegyGrid import StartegyGrid

if __name__ == "__main__":
    # Get json object with the intraday data and another with  the call's metadata
   # data = pd.read_csv(r'C:\Users\Mikolaj\Downloads\daily_IBM.csv')
    #data = pd.read_csv(r'frame.csv')
    #prices = loadData.load_URLStock('670VPCC632C40KBM', 'DOW')
    prices = loadData.load_csv()
    #ru = Run.RunStrategy(prices, Strat.SMAcross())
    #ru.runStrategy()
    grid = StartegyGrid(Strat.SMAcross(), prices)
    grid.setGrid()
    list = grid.runGrid()
    #print(list)
    #print(data.dtypes)
    #print(data)
    