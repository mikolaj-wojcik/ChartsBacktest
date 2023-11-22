from Transaction import buy, sell, closeAllPositions


class RunStrategy:

    def __init__(self, prices, startegy, startBalance=10000, leverage =1, allowShortSell = False):
        self.startBalance = startBalance
        self.strategy = startegy
        self.shortSell = allowShortSell
        self.priceList = prices
        self.positionsList = []
        pass

    def setPrices(self, newPricechart):
        self.priceList = newPricechart
        pass

    def runStrategy(self):
        self.balance = self.startBalance 
        self.positionsList =[]
        lastClose= 0.0
        recomendation = 0
        for singleCandle in self.priceList:
            if(recomendation == 1):
                self.balance, self.positionsList = buy(positions=self.positionsList, balance= self.balance, price= singleCandle.open,allowShort = self.shortSell) 
                print(self.positionsList)
                pass
            elif(recomendation == 2):
                self.balance, self.positionsList = sell(positions=self.positionsList, balance= self.balance, price= singleCandle.open, allowShort = self.shortSell) 
                print(self.positionsList)
                pass
            recomendation, take_profit, stop_loss = self.strategy.onTick(singleCandle) #recomendation 0- hold, 1-buy, 2-sell
            #print(self.balance)
            
            lastClose = singleCandle.close
            pass
        self.balance = closeAllPositions(positions=self.positionsList, balance= self.balance, lastPrice= lastClose)
        print(self.balance)
        return self.balance
    