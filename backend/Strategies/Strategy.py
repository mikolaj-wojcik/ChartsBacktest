
import pandas as pd
from abc import ABC, abstractmethod
import ta

class Strategy(ABC):

    def __init__ (self, prices):
        super().__init__()
        if(prices != None):
            self.prices = prices
        else:
            self.prices = pd.DataFrame()
        pass
    
    def setPrices(self, prices):
        self.prices = prices

    @abstractmethod
    def onTick(self, iter):
        #return 0, 0.0
        return self.prices.iloc[iter]

    def updateIndicators(self, price):
        for indk, indv in self.indicators.items():
            indv.update(price)

    @abstractmethod
    def setParams(self,indicatorParams):
        pass

    @abstractmethod
    def loadPrices(self,prices):
        pass

