import importlib
import os
from os import listdir
from os.path import isfile, join
from xxlimited_35 import error

from OrderProcess import Order
import Statistics.BasicMetrics as basicMetrics
###Avalible data:
###Price history
###Transaction history
###Assets value history
###Balance history
PREDEF_METRICS = {"Gross Profit" : basicMetrics.get_gross_profit,
                  "Gross Loss": basicMetrics.get_gross_loss,
                  "Profit Factor": basicMetrics.get_profit_factor,
                  "Transaction costs": basicMetrics.get_total_comission,
                  "Net Profit": basicMetrics.get_net_profit,
                  "Total trades": basicMetrics.get_total_trades,
                  "Total buying transactions" : basicMetrics.get_total_buying}

#TODO add metrics validation
class CalculateStatistic:


    def __init__(self):
        self.metrics = []
        pass

    def select_stats (self, statistics):
        self.metrics = import_stats(statistics)
        return self.metrics
    pass

    def calculate_performance(self, prices, transactions : list[Order], assets_value=0, balance=0,  starting_balance = 0):
        results_dict = {}
        args_dict = {'prices': prices, 'transactions': transactions, 'assets_value': assets_value, 'balance': balance, 'starting_balance' : starting_balance  }

        for metric in self.metrics:
            try:
                if type(metric) == str:
                    results_dict[metric] = PREDEF_METRICS[metric](args_dict['transactions'])
                    pass
                else:
                    res = metric.calculate(args_dict)
                    results_dict[metric.__name__] = res

            except error:
                print('Metric '+ metric.__name__ +' is not correctly implemented')


        return results_dict

    def calculate_predef_metric(self, metric: str, transactions):
        #gross_profit, gross_loss = get_gross(transactions)
        """
        results_dict["Gross Profit"] = round(gross_profit, 2)
        results_dict["Gross Loss"] = abs(round(gross_loss, 2))
        results_dict["Profit Factor"] = round(gross_profit / (abs(gross_loss) if gross_loss != 0 else 1),
                                              2)  # if gross_loss != 0 else 1), 2)
        results_dict["Transaction costs"] = round(get_total_comission(transactions), 2)
        results_dict["Net Profit"] = round(results_dict["Gross Profit"] - results_dict["Gross Loss"] - results_dict["Transaction costs"], 2)
        results_dict["Total trades"] = len(transactions)
        results_dict["Total buying transactions"] = len(list(filter(lambda x: (x.size > 0), transactions)))
        """


def load_list_of_stat():
    path = os.path.dirname(__file__) + '/Metrics'
    onlyfiles = list(PREDEF_METRICS.keys())
    onlyfiles += [f.split('.')[0] for f in listdir(path) if isfile(join(path, f))]

    return onlyfiles

def is_avalible(selected, fullList):
#Check if input module names exist
     sel = selected.split(' ')
     for s in sel:
        s = s.strip()
        if s not in fullList:
            if s != '':
                print('Metrics ' + s + ' was not found.')
            sel.remove(s)
            corr_input = True
     return sel

def import_stats( to_import):
     sel_modules = list()
     for n in to_import:
         if n not in PREDEF_METRICS.keys():
           try:
             name = 'Statistics.Metrics.' + n.strip()
             module = importlib.import_module(name)
             my_class = getattr(module, n.strip())
             module = my_class()
             sel_modules.append(module)
           except TypeError:
               print('Metric '+ n +' is not correctly implemented')
           except  ModuleNotFoundError:
               print('Module '+ n +' doesnt exist in package Metrics')
           pass
         else:
             sel_modules.append(n)
     return sel_modules




