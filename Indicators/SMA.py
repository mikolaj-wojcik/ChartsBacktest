#open, close, high, low
import itertools

class SMA:
    

    def __init__(self, interval):
        self.interval = interval
        self.priceList = []
        self.value =0.0

    def update(self, price):
        self.priceList.append(price)
        if len(self.priceList)==(self.interval+1):
            self.priceList.pop(0)
            total = 0
            for priceIt in self.priceList:
                total += priceIt
            self.value =  total/self.interval
        

    def SMA(self):
        return self.value