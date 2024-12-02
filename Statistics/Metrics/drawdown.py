import pandas as pd

class drawdown:
    paramsDict = {'BalanceTrack': []}
    __name__ = 'drawdown'
    def __init__(self):
        pass

    def calculate(self, prices_df):
        value = prices_df['portfolio_value']
        curr_max =value[0]
        curr_min = value[0]
        max_dd =0
        for v in value:
            if v > curr_max:
                max_dd = max(max_dd, (curr_max - curr_min)/ curr_max )
                curr_max = v
                curr_min = curr_max
            elif v < curr_min:
                curr_min = v
        return str(round(max_dd*100, 4)) + '%'
        #prices_df['prev_peak']= prices_df['portfolio_value'].cummax()
        #prices_df['draw_down'] = (prices_df['portfolio_value'] - prices_df['prev_peak'])/prices_df['portfolio_value']
        #return max(prices_df['draw_down'])
