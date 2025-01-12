import mplfinance as mpf
import pandas as pd
from matplotlib.pyplot import title, savefig
import os


def create_chart(stockData, transactionHistory, directory):
    markers, colors = create_markers(stockData, transactionHistory.transaction_history)
    stockData = stockData.rename(columns={'date' : 'Date', 'open' : 'Open', 'high' : 'High','low' : 'Low','close' : 'Close', 'vol' : 'Vol' })
    stockData['Datetime'] = pd.to_datetime(stockData['Date'])
    stockData = stockData.set_index(pd.DatetimeIndex(stockData['Datetime']))
    ap = mpf.make_addplot(0.99*stockData['Low'],type='scatter',marker=markers,markersize=45,color=colors)

    if not os.path.exists(directory):
        os.makedirs(directory)
    plot = mpf.plot(stockData, type='line', addplot= ap, title= str(transactionHistory.name)[1:][:1], savefig = directory+ string_from_dict(transactionHistory.name)+ '.png')
    return plot
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

def string_from_dict(dicti, separator =''):
    l_str = ''
    for d in dicti:
        l_str += str(d) + separator +  str(dicti[d])
    return l_str

def clean_dir(directory_path):
    try:
        files = os.listdir(directory_path)
        for file in files:
            file_path = os.path.join(directory_path, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
    except OSError:
        print("Error occurred while deleting files.")