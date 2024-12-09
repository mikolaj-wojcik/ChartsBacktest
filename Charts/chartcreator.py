import mplfinance as mpf
import pandas as pd
from matplotlib.pyplot import title


def create_chart(stockData, transactionHistory):
    markers, colors = create_markers(stockData, transactionHistory[1][2])
    stockData = stockData.rename(columns={'date' : 'Date', 'open' : 'Open', 'high' : 'High','low' : 'Low','close' : 'Close', 'vol' : 'Vol' })
    stockData['Datetime'] = pd.to_datetime(stockData['Date'])
    stockData = stockData.set_index(pd.DatetimeIndex(stockData['Datetime']))
    ap = mpf.make_addplot(0.99*stockData['Low'],type='scatter',marker=markers,markersize=45,color=colors)
    plot = mpf.plot(stockData, type='line', addplot= ap, title= str(transactionHistory[0])[1:][:1])

    pass

def create_markers(stockData, transactionHistory):
    markers = [' '] * len(stockData)
    colors = ['w'] * len(stockData)
    for t in transactionHistory:
        if t.size > 0:
            markers[t.candle] = '$▲$'
            colors[t.candle] = 'g'
        else:
            markers[t.candle] = '$▼$'
            colors[t.candle] = 'r'
        pass
    return markers, colors
    pass