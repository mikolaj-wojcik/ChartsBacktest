#open, close, high, low

def SMA(prices):
    for price in prices:
        total += price
    return total/prices.len()