import pandas as pd
import Indicators.SMA as SMA
import Transaction
import Strategies.Strategy as strat
from ta.trend import SMAIndicator 


class SMAcross (strat.Strategy):
   
    paramsDict = {'shortSMA' : 0, 'longSMA':0}

    def __init__(self, prices = None,indicatorsParams = {'shortSMA':7, 'longSMA':14}, min_position=1):
        super().__init__(prices = prices)
        self.indicatorsParams = indicatorsParams
        
        self.lastShort = 0.0
        self.lastLong = 0.0
        self.min_position = min_position
        if(prices!=None):
            self.calculateIndicators()
        pass

    
    def setParams(self, indicatorParams):

        self.indicatorParams = indicatorParams
        self.lastShort = 0.0
        self.lastLong = 0.0
        if(not self.prices.empty):
            self.calculateIndicators()

    def calculateIndicators(self):
        SMA_short = SMAIndicator(self.prices['close'], self.indicatorsParams['shortSMA'])
        SMA_long = SMAIndicator(self.prices['close'], self.indicatorsParams['longSMA'])
        self.prices['SMAshort'] = SMA_short.sma_indicator()
        self.prices['SMAlong'] = SMA_long.sma_indicator()

    def loadPrices(self, prices):
        super().setPrices(prices)
        print(self.indicatorsParams)
        self.calculateIndicators()
        pass
    
    def onTick(self, iter, budget=None):
        pricesRow = super().onTick(iter)
        currentShort = pricesRow['SMAshort']
        currentLong = pricesRow['SMAlong']
        price = pricesRow['close']
        recomendation =0
        #print("SMA7=", currentShort, "SMA14=", currentLong)
        if(currentShort > currentLong):
            if (self.lastShort <= self.lastLong):
                recomendation = 1
        if(currentShort < currentLong):
            if (self.lastShort >= self.lastLong):
                recomendation = 2
        self.lastShort = currentShort
        self.lastLong = currentLong
        return recomendation, price, 0.0, 0.0
