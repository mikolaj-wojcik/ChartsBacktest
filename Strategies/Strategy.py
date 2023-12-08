import Indicators
import pandas as pd

class Strategy:
    indicators = {}

    def __init__ (self, prices):
        if(prices != None):
            self.prices = prices
        else:
            self.prices = pd.DataFrame()
        pass

    def setPrices(self, prices):
        self.prices = prices

    def onTick(self, iter):
        return self.prices.iloc[iter]

    def updateIndicators(self, price):
        for indk, indv in self.indicators.items():
            indv.update(price)