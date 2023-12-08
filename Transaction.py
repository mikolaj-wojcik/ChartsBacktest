import math

class Transaction():
     def __init__(self):
          pass
     
     def close(self, positions, balance, size, closeBuy, price, leverage = 1):
        if(closeBuy): #close buy
            while(size < 0):
                if(len(positions) > 0):
                    posToClose = positions.pop()
                    if posToClose[0] > -size:
                        positions.append((posToClose[0]+ size, posToClose[1]))
                        balance -= size*price
                        size = 0
                    elif  posToClose[0] <= -size:
                        balance += posToClose[0]*price
                        size+=posToClose[0]
                else:
                    break
            
        else: #close sell
            while(size > 0):
                if(len(positions) > 0):
                    posToClose = positions.pop()
                    if posToClose[0] < -size:
                        positions.append((posToClose[0]- size, posToClose[1]))
                        balance += size*price
                        size = 0
                    elif  posToClose[0] >= -size:
                        balance -= posToClose[0]*price
                        size+=posToClose[0]
                else:
                    break 

        return positions, balance, size
     
    
          
class NoLewerage(Transaction):

    def __init__(self,balance, positions = [], ):
        super().__init__()
        self.positions = positions
        self.balance = balance
        self.equity = balance
        self.floatingPL = 0.0
        self.startBalance = balance
        pass
    
    def reset(self):
        self.balance = self.startBalance
        self.floatingPL =0.0
        self.positions= []
        
    def close(self, positions, balance, size, price):
            self.positions, self.balance, size = super().close(balance = self.balance, price = price, size = -size, clooseBuy = True, positions = self.positions)
            #   while(size > 0):
            #    if(len(positions) > 0):
            #        posToClose = positions.pop()
            #        if posToClose[0] > size:
            #            positions.append((posToClose[0]- size, posToClose[1]))
            #            balance += size*price
            #            size = 0
            #        elif  posToClose[0] <= size:
            #            balance += posToClose[0]*price
            #            size-=posToClose[0]
            #    else:
            #        break



    def buy(self, price, transactionHistory, size = 1.0):
        if(size*price < self.balance):
                self.positions.append((size,price))
                self.balance -= price*size
        else:
                self.balance-= math.floor(self.balance/size) * price
                self.positions.append(math.floor(self.balance/size), price)
        return self.balance, self.positions
    

    def sell(self, price, transactionHistory,size = 1.0):
             while size >0.0:
                 if(len(self.positions) > 0):
                     posToClose = self.positions.pop()
                     if posToClose[0] > size:
                         self.positions.append((posToClose[0]- size, posToClose[1]))
                         self.balance += size*price
                         size = -1
                     elif  posToClose[0] <= size:
                         self.balance += posToClose[0]*price
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
        


    def closeAllPositions(self, positions, balance, lastPrice,toClose):
        assetsVal = 0.0
        if(toClose):
            for pos in self.positions:
                balance += pos[0] * lastPrice
        else:
            for pos in self.positions:
                assetsVal += pos[0] * lastPrice
        return balance, assetsVal  
    
    def checkForStopOut(self, lastPrice):
         return self.balance, self.positions
    
class Lewerage(Transaction):
    def __init__(self, balance, positions = [], leverage=10, stopOut=  0.5  ):
        super().__init__()
        self.equity= balance
        self.balance = balance
        self.floatingPL = 0.0
        self.positions = positions
        self.leverage = leverage
        self.stopOutLevel = stopOut
        self.startBalance = balance
        pass


    def reset(self):
        self.balance = self.startBalance
        self.floatingPL =0.0
        self.positions= []

    def buy(self, price, transactionHistory, size = 1.0):
        if(len(self.positions) != 0):
            if(self.positions[0][0] < 0):
                self.positions, self.balance, size = self.close(positions= self.positions, balance=self.balance, size=size, closeBuy = False, price = price, )
                pass
        if(size > 0):
            
            if(size*price/self.leverage < self.balance):
                self.positions.append((size,price))
                self.balance -= price*size/self.leverage
        return self.balance, self.positions
    
    def sell(self, price, transactionHistory,size = 1.0):
        size *= -1
        if(len(self.positions) != 0):
            if(self.positions[0][0] > 0):
                self.positions, self.balance, size = self.close(positions= self.positions, balance= self.balance, size= size, closeBuy = True, price = price, )
                pass
        if size <0:
             if(-size*price/self.leverage < self.balance):
                self.positions.append((size,price))
                self.balance -= price*size/self.leverage
        return self.balance, self.positions
        
    def close(self, positions, balance, size, closeBuy, price):
        if(closeBuy): #close buy
            while(size < 0):
                if(len(self.positions) > 0):
                    posToClose = self.positions.pop()
                    if posToClose[0] > -size:
                        self.positions.append((posToClose[0]+ size, posToClose[1]))
                        self.balance -= (size*(price - posToClose[1]) + size*posToClose[1]/self.leverage)
                        size = 0
                    elif  posToClose[0] <= -size:
                        self.balance += posToClose[0]*(price-posToClose[1]) + posToClose[0]*posToClose[1]/self.leverage
                        size+=posToClose[0]
                else:
                    break
            
        else: #close sell
            while(size < 0):
                if(len(self.positions) > 0):
                    posToClose = self.positions.pop()
                    if posToClose[0] < -size:
                        self.positions.append((posToClose[0]- size, posToClose[1]))
                        self.balance += size*(posToClose[1] - price) + -size*posToClose[1]/self.leverage
                        size = 0
                    elif  posToClose[0] >= -size:
                        self.balance -= posToClose[0]*(posToClose[1] - price) + posToClose[0]*posToClose[1]/self.leverage
                    
                        size+=posToClose[0]
                else:
                    break 

        return self.positions, self.balance, size

    def closeAllPositions(self, positions, balance, lastPrice,toClose):
        assetsVal = 0.0
        if(toClose):
            for pos in positions:
                balance += pos[0] * lastPrice
        else:
            assetsVal = self.calculateFloating(lastPrice)
        return balance, assetsVal

    def calculateFloating(self, price):
        for transaction in self.positions:
            self.floatingPL += transaction[0] * (price - transaction[1])
        return self.floatingPL
    


    def checkForStopOut(self, lastPrice):
        while(not self.calculateMargin(lastPrice)):
            print(self.positions[0][0])
            if(self.positions[0][0] > 0):
                print(('try to close'))
                self.positions, self.balance, size = self.close(positions= self.positions, balance=self.balance, size=-self.positions[0][0], closeBuy = True, price = lastPrice, )
            else:
                self.positions, self.balance, size = self.close(positions= self.positions, balance= self.balance, size= -self.positions[0][0], closeBuy = False, price = lastPrice, )
            pass

        return self.balance, self.positions
    
    def calculateMargin(self, price): #retur True if no positio reductio is required
        margin = 0.0
        ogMargin = 0.0
        if(len(self.positions) != 0 ):
            margin +=abs(sum(list(map(lambda x: (x[0] * price)/self.leverage, self.positions))))
            ogMargin +=abs(sum(list(map(lambda x: x[0]*x[1] / self.leverage, self.positions))))
            floating = self.calculateFloating(price)
            if(self.stopOutLevel * margin < ogMargin+ floating + self.balance):
                return True
            else:
                return False
        return True