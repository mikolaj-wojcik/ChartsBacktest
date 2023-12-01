import math

def buy(positions, balance, price, transactionHistory, allowShort = False, size = 1.0):
    if(allowShort):


        pass
    else:
        if(size*price < balance):
            positions.append((size,price))
            balance -= price*size
        else:
            balance-= math.floor(balance/size) * price
            positions.append(math.floor(balance/size), price)
    return balance, positions
   

def sell(positions, balance, price, transactionHistory, allowShort = False,size = 1.0):
    if(allowShort):
        pass
    else:
        while size >0.0:
            if(len(positions) > 0):
                posToClose = positions.pop()
                if posToClose[0] > size:
                    positions.append((posToClose[0]- size, posToClose[1]))
                    balance += size*price
                    size = -1
                elif  posToClose[0] <= size:
                    balance += posToClose[0]*price
                    size-=posToClose[0]          
            else:
                break
    return balance, positions
    


def closeAllPositions(positions, balance, lastPrice,toClose):
    assetsVal = 0.0
    if(toClose):
        for pos in positions:
            balance += pos[0] * lastPrice
    else:
        for pos in positions:
            assetsVal += pos[0] * lastPrice
    return balance, assetsVal

def checkForStopOut(balance, postions, lastPrice):

    return balance, postions