import pandas as pd
import Indicators.SMA as SMA
import Transaction
import Strategies.Strategy as strat

class SMAcross (strat.Strategy):
   
    

    def __init__(self, shortSMA=7, longSMA=14, min_position=1):
        super().__init__
        super().indicators['short'] = SMA.SMA(shortSMA)
        super().indicators['longSMA'] = SMA.SMA(longSMA)
        self.openPostitions = []
        self.lastShort = 0.0
        self.lastLong = 0.0
        self.min_position = min_position
        pass

    def run(self, prices, balance, shortInterval, longInterval):
        pass
    
    def onTick(self, price, budget=None):
        super().onTick(price.close)
        currentShort = super().indicators['short'].value
        currentLong = super().indicators['longSMA'].value
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
        return recomendation, 0.0, 0.0
