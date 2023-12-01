from Transaction import buy, sell, closeAllPositions


class RunStrategy:

    def __init__(self, prices, startegy, startBalance=10000, leverage =1, allowShortSell = False, toClose = False):
        self.startBalance = startBalance
        self.strategy = startegy
        self.shortSell = allowShortSell
        self.priceList = prices
        self.positionsList = []
        self.transactionHistory = []
        self.closeAllAfter = toClose

        self.strategy.loadPrices(self.priceList)
        pass

    def setPrices(self, newPricechart):
        self.priceList = newPricechart
        pass

    def runStrategy(self):
        self.balance = self.startBalance 
        self.positionsList =[]
        lastClose= 0.0
        recomendation = 0
        for ind in self.priceList.index:
            if(recomendation == 1):
                self.balance, self.positionsList = buy(positions=self.positionsList, balance= self.balance, price= self.priceList['open'][ind],allowShort = self.shortSell, transactionHistory = self.transactionHistory) 
                print(self.positionsList)
                pass
            elif(recomendation == 2):
                self.balance, self.positionsList = sell(positions=self.positionsList, balance= self.balance, price= self.priceList['open'][ind], allowShort = self.shortSell, transactionHistory= self.transactionHistory) 
                print(self.positionsList)
                pass
            recomendation, price, take_profit, stop_loss = self.strategy.onTick(ind) #recomendation 0- hold, 1-buy, 2-sell
            #print(self.balance)
            
            lastClose = self.priceList['close'][ind]
            pass
        self.balance, assets = closeAllPositions(positions=self.positionsList, balance= self.balance, lastPrice= lastClose, toClose = self.closeAllAfter)
        print("Cash balance: ", self.balance)
        if(not self.closeAllAfter):
            print("Value of assets: ", assets)
        return self.balance
    