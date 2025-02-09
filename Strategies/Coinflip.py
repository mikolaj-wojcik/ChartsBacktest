import pandas as pd
import Transaction
import Strategies.Strategy as strat
from ta.trend import SMAIndicator
import random


class Coinflip(strat.Strategy):
    paramsDict = {'min_holding_period': 0}

    def __init__(self, prices=None, indicatorsParams={'min_holding_period': 3}, min_position=1):
        super().__init__(prices=prices)
        self.indicatorsParams = indicatorsParams
        self.last_transaction = 0
        self.min_position = min_position
        if (prices != None):
            self.calculateIndicators()
        pass

    def setParams(self, indicatorParams):
        pass

    def calculateIndicators(self):
     pass

    def loadPrices(self, prices):
        super().setPrices(prices)
        pass

    def onTick(self, iter, budget=None):
        pricesRow = super().onTick(iter)
        recomendation =0
        price = pricesRow['close']
        if self.indicatorsParams['min_holding_period'] < self.last_transaction:
            ran =  random.randint(1,100)
            if ran  == 10:
                self.last_transaction = 0
                recomendation =1
            elif ran == 20:
                self.last_transaction = 0
                recomendation =2
        self.last_transaction += 1
        return recomendation, price, 100.0, 100.0
