from dataclasses import dataclass
from datetime import datetime
import pandas as pd
import re

@dataclass
class priceStruct:
    open: float
    high: float
    low: float
    close: float
    date: datetime.date

   # def __init__():
   #     pass

    def __init__(self, open: float, high: float, low: float, close: float, date: datetime.date):
        self.open = open
        self.close = close
        self.high = high
        self.low = low
        self.date = date

    def setPrices(self, open: float, high: float, low: float, close: float):
        self.open = open
        self.close = close
        self.high = high
        self.low = low


def generatePriceListFromDf(dataframe: pd.DataFrame) ->list :
    pricesList = []
    dateFormatWithTime = r'%Y-%m-%d %H:%M:%S'
    dateFormatNoTime = '%Y-%m-%d'
    for ind in dataframe.index:
        dateString = str(dataframe['timestamp'][ind])
        if re.search('\s', dateString) != None :
            date = datetime.strptime(dateString, dateFormatWithTime)
        else:
            date = datetime.strptime(dateString, dateFormatNoTime)
        singPrice= priceStruct(open = dataframe['open'][ind], high= dataframe['high'][ind], low= dataframe['low'][ind], close= dataframe['close'][ind], date= date)
        pricesList.append(singPrice)

    return pricesList
