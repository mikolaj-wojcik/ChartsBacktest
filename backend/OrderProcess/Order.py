from enum import Enum



class Order():
    def __init__(self, size, side, oType,protectionOrder :dict,  price=0.0, candle = None, commission = 0, profit = 0.0 ) -> None:
        self.price = price
        self.size = size
        self.candle  = candle
        self.closeCandle = None
        self.direction = side
        self.closePrice = None
        self.orderType = oType
        self.stopLoss =0.0
        self.takeProfit = 0.0
        self.commission = commission
       # if(protectionOrder):
        if protectionOrder['stop loss'] != 0.0:
            if((self.direction == Direction.BUY and self.price > protectionOrder['stop loss']) or (self.direction == Direction.SELL and self.price <protectionOrder['stop loss'])):
                self.stopLoss = protectionOrder['stop loss']
        if protectionOrder['take profit'] != 0.0:
            if((self.direction == Direction.BUY and self.price < protectionOrder['take profit']) or (self.direction == Direction.SELL and self.price > protectionOrder['take profit'])):
                self.takeProfit = protectionOrder['take profit']

    def setStopLoss(self, openPrice, stopLoss):
        if(self.direction == Direction.BUY):
            if(stopLoss < openPrice):
                self.stopLoss = stopLoss
            pass
        elif(self.direction == Direction.SELL):
            if(stopLoss > openPrice):
                self.stopLoss = stopLoss
            pass
        pass
    
    def setTakeProfit(self, openPrice ,takeProfit):
        if(self.direction == Direction.BUY):
            if(takeProfit > openPrice):
                self.takeProfit = takeProfit
            pass
        elif(self.direction == Direction.SELL):
            if(takeProfit < openPrice):
                self.takeProfit = takeProfit
            pass
        pass

    def setClosePriceAndCandle(self, price, candle):
        self.closePrice = price
        self.closeCandle = candle

    def setSize(self, size):
        self.size = size
    def checkTpSlHit(self, priceBar):
        returnPrice = None
        openP = priceBar['open']
        high = priceBar['high']
        low = priceBar['low']

    #Limit orders (TakeProfits) 
        if self.direction is Direction.BUY:
            if high < self.takeProfit:
                returnPrice = openP
            elif self.takeProfit >= low:
                if openP < self.takeProfit:  
                    returnPrice = openP
                else:
                    returnPrice = self.takeProfit
        elif self.direction is Direction.Sell:
            if low > self.takeProfit:
                returnPrice = openP
            elif self.takeProfit <= high:
                if openP > self.takeProfit:  
                    returnPrice = openP
                else:
                    returnPrice = self.takeProfit

    #Stop orders (StopLosses)
         
        if self.direction is Direction.BUY:
            if low > self.stopLoss:
                returnPrice = openP
            elif self.stopLoss <= high:
                if openP > self.stopLoss: 
                    returnPrice = openP
                else:
                    returnPrice = self.stopLoss
       
        elif self.direction is Direction.SELL:
            if high < self.stopLoss:
                returnPrice = openP
            elif self.stopLoss >= low:
                if openP < self.stopLoss: 
                    returnPrice = openP
                else:
                    returnPrice = self.stopLoss

        return returnPrice

class ClosedOrder():
    def __init__(self, candle, size, price, commission, profit = 0.0, balance = 0.0):
        self.candle = candle
        self.size = size
        self.price = price
        self.commission = commission
        self.profit = profit
        self.balance = balance

class Direction(Enum):
    BUY = 'buy'
    SELL = 'sell'

class Status(Enum):
    PENDING = 0
    FILLED = 1

class OrderType(Enum):
    MARKET = 'market'
    LIMIT = 'limit'
    STOP =  'stop'
