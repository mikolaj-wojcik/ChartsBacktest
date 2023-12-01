import Indicators

class Strategy:
    indicators = {}

    def __init__ (self, prices):

        self.prices = prices
        pass

    def setPrices(self, prices):
        self.prices = prices

    def onTick(self, iter):
        return self.prices.iloc[iter]

    def updateIndicators(self, price):
        for indk, indv in self.indicators.items():
            indv.update(price)