from Transaction import Lewerage, NoLewerage


class RunStrategy:

    def __init__(self, prices, startegy = None, startBalance=10000, leverage =1, allowShortSell = False, toClose = False):
        self.startBalance = startBalance
        self.strategy = startegy
        self.shortSell = allowShortSell
        self.priceList = prices
        self.positionsList = []
        self.transactionHistory = []
        self.closeAllAfter = toClose
        #self.transaction = Lewerage(startBalance, leverage= 10)
        self.transaction = NoLewerage(startBalance)
        self.setStrategy(startegy)
        pass

    def setPrices(self, newPricechart):
        self.priceList = newPricechart
        if(self.strategy):
            
            self.strategy.loadPrices(self.priceList)
        pass

    def setStrategy(self, strateggy):
        self.strategy  = strateggy
        if(self.strategy):
            self.strategy.loadPrices(self.priceList)

    def runStrategy(self):
        if (self.strategy == None):
            return
        self.balance = self.startBalance 
        self.transaction.reset()
        self.positionsList =[]
        lastClose= 0.0
        recomendation = 0
        for ind in self.priceList.index:
            if(recomendation == 1):
                self.balance, self.positionsList = self.transaction.buy(price= self.priceList['open'][ind], transactionHistory = self.transactionHistory) 
                #print(self.positionsList)
                pass
            elif(recomendation == 2):
                self.balance, self.positionsList = self.transaction.sell( price= self.priceList['open'][ind], transactionHistory= self.transactionHistory) 
                #print(self.positionsList)
                pass
            recomendation, price, take_profit, stop_loss = self.strategy.onTick(ind) #recomendation 0- hold, 1-buy, 2-sell
            #self.balance, self.positionsList = self.transaction.checkForStopOut(self.priceList['open'][ind])
            #print(self.balance)
            
            lastClose = self.priceList['close'][ind]
            pass
        self.balance, assets = self.transaction.closeAllPositions(positions=self.positionsList, balance= self.balance, lastPrice= lastClose, toClose = self.closeAllAfter)
        print("Cash balance: ", self.balance, assets)
        #if(not self.closeAllAfter):
        #    print("Value of assets: ", assets)
        print(self.positionsList)
        return self.balance, assets
    


    