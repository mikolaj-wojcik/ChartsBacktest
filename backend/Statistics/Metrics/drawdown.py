

class drawdown:
    __name__ = 'drawdown'
    def __init__(self):
        pass

    def calculate(self, args_dict, ):
        prices_df = args_dict['prices']
        value = prices_df['portfolio_value']
        peak = value[0]
        max_dd = 0

        for v in value:
            if v > peak:
                peak = v
            current_dd = (peak - v) / peak
            max_dd = max(max_dd, current_dd)
        return round(max_dd*100, 4)

