import pandas as pd
import Indicators.SMA as SMA
import Transaction

class SMAcross:
    openPostitions = []
    shortInterval = 0
    longInterval = 0
    lastShort = 0
    

    def __init__(self):
        pass

    def run(self, prices, balance, shortInterval, longInterval):
        self.shortInterval = shortInterval
        self.longInterval = longInterval

        for i in range(len(prices)):
            print(list[i])


        return balance
    
    def onTick(self, price, budget, ):
        recomendation: str
        return recomendation, size
