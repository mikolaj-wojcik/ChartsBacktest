from RunStrategy import RunStrategy



#from Statistics.CalculateStatistic import CalculateStatistic


class StartegyGrid():

    def __init__(self, strategy, prices, starting_balance = 10000):
        self.strategy = strategy
        self.paramGrid = {}
        self.paramDict = strategy.paramsDict
        self.prices = prices
        self.resultList = []
        self.run = RunStrategy.RunStrategy(prices, startBalance = starting_balance)
        print(type(strategy.paramsDict))

    def setGrid(self):
        paramGrid = {}
        print('Enter in format \'min\', \'max\', \'step\'')
        for key, val in self.paramDict.items():
            print('Set value for ', key,':  value type ', type(val))
            a = input( )
            if(type(val) == int):
                paramGrid[key] = tuple(int(x) for x in a.split(","))
            else:
                paramGrid[key] = tuple(float(x) for x in a.split(","))

        self.paramGrid = paramGrid


    def runGrid(self):
        
        self.generate_combinations(self.paramGrid)



        return  self.resultList
        
    def generate_combinations(self, params_dict, current_combination=None, keys=None):
        if current_combination is None:
            current_combination = {}
        if keys is None:
            keys = list(params_dict.keys())
        if not keys:
           # print(current_combination)
            self.strategy.setParams(current_combination)
            self.run.setStrategy(self.strategy)
            temp = current_combination.copy()
            results_tuple = self.run.runStrategy()
            self.resultList.append(single_strategy(temp, results_tuple[0], results_tuple[1], results_tuple[2], results_tuple[3])) #<- running strategy Combination + balance + assets + transactionhistory(class ClosedOrder) + df_prices_balanceHistory
            return

        current_key = keys[0]
        tempTuple = params_dict[current_key]
        if(len(tempTuple) == 1):
            current_combination[current_key] = tempTuple
            self.generate_combinations(params_dict, current_combination, keys[1:])
            
        else:
            start, stop, step = tempTuple
            if(type(start) == float):
                paras_list = map(lambda x: x/100.0, range(start*100, stop*100 +1, step*100))
                for value in paras_list:
                    current_combination[current_key] = value
                    self.generate_combinations(params_dict, current_combination, keys[1:])
            else:
                for value in range(start, stop + 1, step):
                    current_combination[current_key] = value
                    self.generate_combinations(params_dict, current_combination, keys[1:])


class single_strategy:

    def __init__(self, name,balance, assets, transaction_history, prices):
        self.name = name
        self.prices = prices
        self.statistics = None
        self.transaction_history = transaction_history
        self.balance = balance
        self.assets = assets


    def setStatistics(self, statistics):
        self.statistics = statistics