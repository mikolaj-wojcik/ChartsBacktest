from backend.Transaction import Lewerage, NoLewerage


class RunStrategy:

    def __init__(self, prices, startegy = None, startBalance=10000, min_commission = 1.0, commission_factor = 0.01, leverage =1, allowShortSell = False, toClose = True):
        self.startBalance = startBalance
        self.strategy = startegy
        self.shortSell = allowShortSell
        self.priceList = prices
        self.positionsList = []
        self.transactionHistory = []
        self.closeAllAfter = toClose
        self.balanceTrack = []
        self.transaction = NoLewerage(startBalance, min_commission= min_commission, commission_factor= commission_factor)
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
        self.transactionHistory = []
        self.balanceTrack = []
        lastClose= 0.0
        recomendation = 0
        size = 0.0
        for ind in self.priceList.index:
            if self.transaction.__class__ == Lewerage:
                self.balance, self.positionsList = self.transaction.checkForStopOut(candle=ind, price=self.priceList['open'][ind], lastPrice=self.priceList.iloc[ind-1])
            if(recomendation == 1):
                self.balance, self.positionsList = self.transaction.buy(price= self.priceList['open'][ind], candle=ind, transactionHistory = self.transactionHistory, size = size)
                pass
            elif(recomendation == 2):
                self.balance, self.positionsList = self.transaction.sell( price= self.priceList['open'][ind],candle =ind, transactionHistory= self.transactionHistory,size = size)
                pass
            recomendation, size  = self.strategy.onTick(ind) #recomendation 0- hold, 1-buy, 2-sell

            self.balanceTrack.append(self.balance + sum(float(quantity*self.priceList['close'][ind])  for quantity, opPrice in self.positionsList))
            lastClose = self.priceList['close'][ind]
            pass
        self.balance, assets = self.transaction.closeAllPositions(positions=self.positionsList, balance= self.balance, candle = ind,lastPrice= lastClose, toClose = self.closeAllAfter)
        tmp_prices = self.priceList.copy()
        tmp_prices['portfolio_value'] = self.balanceTrack
        return self.balance, assets, self.transaction.history, tmp_prices
    


    