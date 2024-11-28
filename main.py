import pandas as pd
#import yfinance as yf
import requests
import datetime

from samba.dcerpc.nbt import statistics

#from alpha_vantage.timeseries import TimeSeries
#from alpha_vantage.cryptocurrencies import CryptoCurrencies
#from alpha_vantage.foreignexchange import ForeignExchange
import loadData
import Strategies.SMAcross as Strat
import RunStrategy.RunStrategy as Run
from RunStrategy.StartegyGrid import StartegyGrid
from SelectStrategy import SelectStrategy
from Statistics.CalculateStatistic import CalculateStatistic

if __name__ == "__main__":
    # Get json object with the intraday data and another with  the call's metadata
   # data = pd.read_csv(r'C:\Users\Mikolaj\Downloads\daily_IBM.csv')
    #data = pd.read_csv(r'frame.csv')
    #prices = loadData.load_URLStock('670VPCC632C40KBM', 'DOW')
    prices = loadData.load_csv()
    #ru = Run.RunStrategy(prices, Strat.SMAcross())
    #ru.runStrategy()
    strat = SelectStrategy(True)
    if(strat != 0):
        grid = StartegyGrid(strat, prices)
        grid.setGrid()
        list = grid.runGrid()
        statistics = CalculateStatistic()

        statistics.calculate(list, statistics.selectStats())

    #print(list)
    #print(data.dtypes)
    #print(data)
    