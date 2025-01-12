import pandas as pd
#import yfinance as yf
import requests
import datetime

#from alpha_vantage.timeseries import TimeSeries
#from alpha_vantage.cryptocurrencies import CryptoCurrencies
#from alpha_vantage.foreignexchange import ForeignExchange
import loadData
import Strategies.SMAcross as Strat
import RunStrategy.RunStrategy as Run
from RunStrategy.StartegyGrid import StartegyGrid, single_strategy
from SelectStrategy import SelectStrategy
from Statistics.CalculateStatistic import CalculateStatistic

import Charts.chartcreator as chart
from save_to_file import save_to_file

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
        starting_balance = 10000
        grid = StartegyGrid(strat, prices, starting_balance= starting_balance)
        grid.setGrid()
        print("Calculating...")
        list_strat = grid.runGrid()
        statistics = CalculateStatistic()
        statistics.select_stats()
        stats_and_plots = []
        for strat in list_strat:
            strat.setStatistics(statistics.calculate_performance(strat.prices, transactions=strat.transaction_history, balance= strat.balance, starting_balance = starting_balance))
            #strat struct: name(dict) (prices etc.) (statiscts dict)
            #strat
        print("Generating document...")
        save_to_file(list_strat, stats_and_plots,prices, '0')

    #print(list)
    #print(data.dtypes)
    #print(data)
    