import math

from backend.OrderProcess.Order import ClosedOrder


class Transaction():
    def __init__(self, balance, positions, min_commission, commission_factor, leverage):
        self.history =[] ###candle number, size, price of trasaction, 
        self.balance = balance
        self.positions = positions
        self.leverage = leverage
        self.equity = balance
        self.floatingPL = 0.0
        self.startBalance = balance
        self.min_commission = min_commission
        self.commission_factor = commission_factor
        pass

    def reset(self):
        self.balance = self.startBalance
        self.floatingPL =0.0
        self.positions= []
        self.history=[]

    def buy(self, price,candle, transactionHistory,  size = 1.0,takeProfit = 0.0, stopLoss = 0.0):
        pass

    def sell(self, price, candle, transactionHistory, size=1.0, takeProfit=0.0, stopLoss=0.0):
        pass

    def closeAllPositions(self, positions, balance, candle, lastPrice, toClose):
        pass

    def commission(self, value):
        if value * self.commission_factor > 0:
            return max(value * self.commission_factor, self.min_commission)
        else:
            return 0.0

    def close(self, positions, balance, size, closeBuy,candle,  price, leverage = 1):
        if(closeBuy): #close buy
            while(size < 0):
                if(len(positions) > 0):
                    posToClose = positions.pop()
                    if posToClose[0] > -size:
                        positions.append((posToClose[0]+ size, posToClose[1]))
                        balance -= size*price
                        self.history.append((candle, size, price, 0.0))
                        size = 0
                    elif  posToClose[0] <= -size:
                        balance += posToClose[0]*price
                        size+=posToClose[0]
                        self.history.append((candle, posToClose[0], price, 0.0, 0.0))
                else:
                    break
            
        else: #close sell
            while(size > 0):
                if(len(positions) > 0):
                    posToClose = positions.pop()
                    if posToClose[0] < -size:
                        positions.append((posToClose[0]- size, posToClose[1]))
                        self.history.append((candle, size, price, ))
                        balance += size*price
                        size = 0
                    elif  posToClose[0] >= -size:
                        balance -= posToClose[0]*price
                        size+=posToClose[0]
                        self.history.append((candle, posToClose[0], price))
                else:
                    break 

        return positions, balance, size
     

    def selectLowPrice(self,  orderPrice, lastPrice, price):

        if(lastPrice['low'] > orderPrice):
            return price
        else:
            return orderPrice

        pass

    def selectHighPrice(self,  orderPrice, lastPrice, price):
        if(lastPrice['high'] < orderPrice):
            return price
        else:
            return orderPrice
    
    def closeSpecPosition(self,candle, positionIndex, price):
            posToClose = self.positions.pop(positionIndex)
            self.balance+= (price - posToClose[1])*posToClose[0] + abs(posToClose[0]*posToClose[1]/self.leverage)
            self.history.append((candle, -posToClose[0], price))
            pass
    
    def checkForSlTp(self, candle, price, lastPrice):
        for ind, pos in enumerate(self.positions):
            if (pos[2] != 0.0):
                if(pos[0] > 0):
                    if(max(lastPrice['high'], price) >= pos[2]):
                        print('Take profit')
                        orderPrice = self.selectHighPrice(lastPrice=lastPrice, price=price, orderPrice= pos[2])
                        self.closeSpecPosition(candle, ind, orderPrice)
                        
                else:
                    if(min(lastPrice['low'], price) <= pos[2]):  
                        orderPrice = self.selectLowPrice(lastPrice=lastPrice, price=price, orderPrice= pos[2])
                        self.closeSpecPosition(candle, ind, orderPrice)
                        
                
            if(pos[3]!= 0.0):
                if(pos[0] > 0):
                    if(max(lastPrice['low'], price) <= pos[3]):
                        print('Stop loss')
                        orderPrice = self.selectLowPrice(lastPrice=lastPrice, price=price, orderPrice= pos[3])
                        self.closeSpecPosition(candle, ind, orderPrice)
                        
                        
                else:
                    if(min(lastPrice['high'], price) >= pos[3]):  
                        orderPrice = self.selectHighPrice(lastPrice=lastPrice, price=price, orderPrice= pos[3])
                        self.closeSpecPosition(candle, ind, orderPrice)
                        
                pass
            pass
        return self.balance, self.positions
        
    
          
class NoLewerage(Transaction):

    def __init__(self,balance, min_commission =1.0, commission_factor = 0.01, positions = [], ):
        super().__init__(balance, positions, min_commission, commission_factor, 1)
        
        self.marginPrice = 0.0
  
        pass
    
        
    def close(self, positions,candle, balance, size, price):
            self.positions, self.balance, size = super().close(balance = self.balance, price = price, size = -size, clooseBuy = True, positions = self.positions)
            



    def buy(self, price,candle, transactionHistory,  size = 1.0,takeProfit = 0.0, stopLoss = 0.0):
        potential_commission = self.commission(size * price)
        if(size*price < self.balance):
                self.positions.append((size,price))
                self.balance -= (price*size + potential_commission)
                self.history.append(ClosedOrder(candle, size, price, potential_commission , 0))
        else:
                size = math.floor(self.balance/price)
                potential_commission = self.commission(size * price)
                self.balance-= size * price + potential_commission
                self.positions.append((size, price))
                self.history.append(ClosedOrder(candle, size, price, potential_commission, 0.0))
        return self.balance, self.positions
    

    def sell(self, price,candle, transactionHistory, size = 1.0,takeProfit = 0.0, stopLoss = 0.0):
             while size >0.0:
                 if(len(self.positions) > 0):
                     posToClose = self.positions.pop()
                     if posToClose[0] > size:
                         potential_commission = self.commission(size * price)
                         self.positions.append((posToClose[0]- size, posToClose[1]))
                         self.history.append(ClosedOrder(candle, -size, price, potential_commission, (price - posToClose[1]) * size))
                         self.balance += size*price - potential_commission
                         size = -1
                     elif  posToClose[0] <= size:
                         potential_commission = self.commission(posToClose[0] * price)
                         self.balance += posToClose[0]*price - potential_commission
                         self.history.append(ClosedOrder(candle, -posToClose[0], price, potential_commission,(price - posToClose[1]) * posToClose[0]))
                         size-=posToClose[0]          
                 else:
                     break
            #self.positions, self.balance, size = super().close(balance = self.balance, closeBuy = True, price = price, size = -size, positions = self.positions)
             return self.balance, self.positions, 
        

    def calculateFloating(self, price):
        floatingPL = self.balance
        for pos in self.positions:
            floatingPL += pos[0] * price
        self.floatingPL = floatingPL
        return self.floatingPL
        


    def closeAllPositions(self, positions, balance, candle,lastPrice,toClose):
        assetsVal = 0.0
        if(toClose):
            for pos in self.positions:
                potential_commission = self.commission(pos[0]*lastPrice)
                balance += pos[0] * lastPrice  - potential_commission
                self.history.append(ClosedOrder(candle, -pos[0], lastPrice, potential_commission, (lastPrice - pos[1]) * pos[0]))
        else:
            for pos in self.positions:
                assetsVal += pos[0] * lastPrice
        return balance, assetsVal  
    
    def checkForStopOut(self, canndle, lastPrice):
         return self.balance, self.positions
    
class Lewerage(Transaction):
    def __init__(self, balance, positions = [], leverage=10, stopOut=  0.5  ):
        super().__init__(balance, positions, leverage)
        
        self.stopOutLevel = stopOut
        pass


    def buy(self, price, transactionHistory, candle,  size = 1000.0, takeProfit = 0.0, stopLoss = 0.0):
        if(len(self.positions) != 0):
            if(self.positions[0][0] < 0):
                self.positions, self.balance, size = self.close(positions= self.positions, balance=self.balance, size=size,candle =candle, closeBuy = False, price = price, )
                
                pass
        if(size > 0):
            
            if(size*price/self.leverage < self.balance):
                self.positions.append((size,price, takeProfit, stopLoss))
                self.history.append((candle, size, price))
                self.balance -= price*size/self.leverage
        return self.balance, self.positions
    
    def sell(self, price, transactionHistory, candle, size = 1.0, takeProfit = 0.0, stopLoss =0.0):
        size *= -1
        if(len(self.positions) != 0):
            if(self.positions[0][0] > 0):
                self.positions, self.balance, size = self.close(positions= self.positions, balance= self.balance, size= size, candle =candle,closeBuy = True, price = price, )
                pass
        if size <0:
             if(-size*price/self.leverage < self.balance):
                self.positions.append((size,price, takeProfit, stopLoss))
                self.balance -= price*size/self.leverage
                self.history.append((candle, size, price))
        return self.balance, self.positions
        
    def close(self, positions, balance, size, candle,  closeBuy, price):
        if(closeBuy): #close buy
            while(size < 0):
                if(len(self.positions) > 0):
                    posToClose = self.positions.pop()
                    if posToClose[0] > -size:
                        self.positions.append((posToClose[0]+ size, posToClose[1]))
                        self.balance -= (size*(price - posToClose[1]) + size*posToClose[1]/self.leverage)
                        self.history.append((candle, size, price))
                        size = 0
                    elif  posToClose[0] <= -size:
                        self.balance += posToClose[0]*(price-posToClose[1]) + posToClose[0]*posToClose[1]/self.leverage
                        size+=posToClose[0]
                        self.history.append((candle, -posToClose[0], price))
                else:
                    break
            
        else: #close sell
            while(size > 0):
                if(len(self.positions) > 0):
                    posToClose = self.positions.pop()
                    if posToClose[0] < -size:
                        self.positions.append((posToClose[0]- size, posToClose[1]))
                        self.balance += size*(posToClose[1] - price) + -size*posToClose[1]/self.leverage
                        self.history.append((candle, size, price))
                        size = 0
                    elif  posToClose[0] >= -size:
                        self.balance -= posToClose[0]*(posToClose[1] - price) + posToClose[0]*posToClose[1]/self.leverage
                    
                        size+=posToClose[0]
                        self.history.append((candle, -posToClose[0], price))
                else:
                    break 

        return self.positions, self.balance, size

    def closeAllPositions(self, positions, balance,candle, lastPrice,toClose):
        assetsVal = 0.0
        if(toClose):
            for pos in positions:
                side =  pos[0] > 0.0
                if side:
                    self.positions, self.balance, size = self.close(positions= self.positions, balance= self.balance, size= -pos[0], candle =candle,closeBuy = side, price = lastPrice, )
                else:
                    self.positions, self.balance, size = self.close(positions= self.positions, balance= self.balance, size= -pos[0], candle =candle,closeBuy = side, price = lastPrice, )
        else:
            assetsVal = self.calculateFloating(lastPrice)
        return balance, assetsVal

    def calculateFloating(self, price):
        self.floatingPL = 0.0
        for transaction in self.positions:
            self.floatingPL += transaction[0] * (price - transaction[1])
        return self.floatingPL
    


    def checkForStopOut(self, candle, price, lastPrice):
        while(not self.calculateMargin(price)):
            print(self.positions)
            if(self.positions[0][0] > 0):
                liqPrice = self.selectLowPrice(self.marginPrice, lastPrice, price)
                #liqPrice = self.selectLowPrice(False, liqPrice, price, lastPrice)
                self.positions, self.balance, size = self.close(positions= self.positions, balance=self.balance, size=-self.positions[0][0], candle= candle,closeBuy = True, price = liqPrice, )
            else:
                liqPrice = self.selectHighPrice(self.marginPrice, lastPrice, price)
                #liqPrice = self.selectHighPrice(False, liqPrice, price, lastPrice)
                self.positions, self.balance, size = self.close(positions= self.positions, balance= self.balance, size= -self.positions[0][0],  candle= candle,closeBuy = False, price = liqPrice, )
            pass

        return self.balance, self.positions
    
    def calculateMargin(self, price): #retur True if no positio reductio is required
        margin = 0.0
        ogMargin = 0.0
        if(len(self.positions) != 0 ):
            margin +=abs(sum(list(map(lambda x: x[0] * price /self.leverage, self.positions))))
            ogMargin +=abs(sum(list(map(lambda x: x[0]*x[1] / self.leverage, self.positions))))
            floating = self.calculateFloating(price)
            self.marginPrice = self.stopOutLevel * margin
            if(self.stopOutLevel * margin < ogMargin+ floating + self.balance):
                return True
            else:
                return False
        return True
    
    def calculateMargin(self, price): #retur True if no positio reductio is required
        #margin = 0.0
        #ogMargin = 0.0
        if(len(self.positions) != 0 ):
            a =abs(sum(list(map(lambda x: x[0] , self.positions))))
            b =abs(sum(list(map(lambda x: x[0]*x[1], self.positions))))
            floating = self.calculateFloating(price)
            self.marginPrice = ((b/self.leverage) - b + self.balance)/((a*self.stopOutLevel/self.leverage)-a)
            if(self.positions[0][0] > 0):
                if(self.marginPrice < price):
                    return True
                else:
                    return False
            else:
                if(self.marginPrice > price):
                    return True
                else:
                    return False
        return True