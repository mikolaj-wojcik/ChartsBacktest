import Transaction 

class RunStrategy:
    balance = 0.0
    transactionList = []
    def __init__(self, startBalance, prices, startegy, allowShortSell = False):
        self.startBalance = startBalance
        self.strategy = startegy
        self.shortSell = allowShortSell
        self.priceChart = prices
        pass

    def setPrices(self, newPricechart):
        self.priceChart = newPricechart
        pass

    def runStrategy(self, **strategyArguments):
        self.balance = self.startBalance 
        self.balance, self.transactionList = self.strategy.run(strategyArguments,prices = self.prices, balance = self.balance)
        print(self.balance)
        pass
    