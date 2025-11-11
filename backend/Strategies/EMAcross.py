import pandas as pd
import Transaction
import Strategies.Strategy as strat
from ta.trend import EMAIndicator


class EMAcross(strat.Strategy):
    paramsDict = {'shortEMA': 0, 'longEMA': 0}

    def __init__(self, prices=None, indicatorsParams={'shortEMA': 7, 'longEMA': 14}, min_position=1):
        super().__init__(prices=prices)
        self.indicatorsParams = indicatorsParams
        self.lastShort = 0.0
        self.lastLong = 0.0
        self.min_position = min_position
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
        EMA_short = EMAIndicator(self.prices['close'], self.indicatorsParams['shortEMA'])
        EMA_long = EMAIndicator(self.prices['close'], self.indicatorsParams['longEMA'])
        self.prices['EMAshort'] = EMA_short.ema_indicator()
        self.prices['EMAlong'] = EMA_long.ema_indicator()

    def loadPrices(self, prices):
        super().setPrices(prices)
        self.calculateIndicators()
        pass

    def onTick(self, iter, budget=None):
        pricesRow = super().onTick(iter)
        currentShort = pricesRow['EMAshort']
        currentLong = pricesRow['EMAlong']
        price = pricesRow['close']
        recomendation = 0
        size = 1.0
        # print("SMA7=", currentShort, "SMA14=", currentLong)
        if (currentShort > currentLong):
            if (self.lastShort <= self.lastLong):
                recomendation = 1
                size =1.0
        if (currentShort < currentLong):
            if (self.lastShort >= self.lastLong):
                recomendation = 2
                size = 1.0
        self.lastShort = currentShort
        self.lastLong = currentLong
        return recomendation, size


