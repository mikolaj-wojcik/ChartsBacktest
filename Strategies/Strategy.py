import Indicators

class Strategy:
    indicators = {}

    def __init__ (self):
        pass

    def onTick(self, price):
        self.updateIndicators(price)

    def updateIndicators(self, price):
        for indk, indv in self.indicators.items():
            indv.update(price)