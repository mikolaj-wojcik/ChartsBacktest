import pandas as pd

import Strategies.Strategy  as strat
from ta.trend import SMAIndicator


class PalceholderStartegy(strat.Strategy):
    paramsDict = {'shortSMA': 0, 'longSMA': 0, 'param1' : 0.0, 'param2' : 0, 'param3' : 0, 'param4' : 0, 'param5' : 0}

    def __init__(self, prices=None, indicatorsParams={'shortSMA': 7, 'longSMA': 14}):
        super().__init__(prices=prices)
        self.indicatorsParams = indicatorsParams
        self.lastShort = 0.0
        self.lastLong = 0.0
        if (prices != None):
            self.calculateIndicators()
        pass

    def setParams(self, indicatorParams):
        self.indicatorsParams = indicatorParams
        self.lastShort = 0.0
        self.lastLong = 0.0
        if (not self.prices.empty):
            self.calculateIndicators()

    def calculateIndicators(self):
        sma_short = SMAIndicator(self.prices['close'], self.indicatorsParams['shortSMA'])
        sma_long = SMAIndicator(self.prices['close'], self.indicatorsParams['longSMA'])
        self.prices['SMAshort'] = sma_short.sma_indicator()
        self.prices['SMAlong'] = sma_long.sma_indicator()

    def loadPrices(self, prices):
        super().setPrices(prices)
        self.calculateIndicators()
        pass

    def onTick(self, iter):
        pricesRow = super().onTick(iter)
        currentShort = pricesRow['SMAshort']
        currentLong = pricesRow['SMAlong']
        price = pricesRow['close']
        recomendation = 0
        size = 1.0
        # print("SMA7=", currentShort, "SMA14=", currentLong)
        if (currentShort > currentLong):
            if (self.lastShort <= self.lastLong):
                recomendation = 1
                size = 1.0
        if (currentShort < currentLong):
            if (self.lastShort >= self.lastLong):
                recomendation = 2
                size = 1.0
        self.lastShort = currentShort
        self.lastLong = currentLong
        return recomendation, size
