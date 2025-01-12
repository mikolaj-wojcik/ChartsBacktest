import importlib
import sys
import os
from inspect import isclass
from os import listdir
from os.path import isfile, join
from xxlimited_35 import error
from OrderProcess import Order


import Statistics.Metrics.PerformanceMetrics
import inspect
import Statistics


###Avalible data:
###Price history
###Transaction history
###Assets value history
###Balance history
###TODO benchmark prices
class CalculateStatistic:
    def __init__(self):
        self.metrics = []
        pass

    def select_stats (self):
        list_avalible_stats = load_list_of_stat()
        print('Select stats to measure performance of strategy.\nUse commas to separate elements.\nAvailable stats are:')
        print (*list_avalible_stats, sep = ', ')

        selected_elements = input('')
        imported_metrics = is_avalible(selected_elements, list_avalible_stats)
        if len(imported_metrics) == 0 :
            #imported_metrics = self.select_stats()
            pass
        self.metrics = import_stats(imported_metrics)
        return self.metrics
    pass

    def calculate_performance(self, prices, transactions : list[Order], assets_value=0, balance=0,  starting_balance = 0):
        results_dict = {}
        args_dict = {'prices': prices, 'transactions': transactions, 'assets_value': assets_value, 'balance': balance, 'starting_balance' : starting_balance  }

        results_dict["Balance"] = round(balance,2)
        results_dict["Gross Profit"] = round((balance - starting_balance), 2)
        results_dict["Total Commission"] = round(get_total_comission(transactions),2)
        results_dict["Net Profit"] = round(balance - starting_balance - results_dict["Total Commission"], 2)
        results_dict["Total trades"] = len(transactions)
        results_dict["Total buying transactions"] = len(list(filter( lambda x : (x.size > 0), transactions)))
   #     results_dict["Total volume"] = sum(sum(filter( lambda x : (x.size > 0), transactions))transactions.size)


        for metric in self.metrics:
            try:
                res = metric.calculate(args_dict)
                results_dict[metric.__name__] = res

            except error:
                print('Metric '+ metric.__name__ +' is not correctly implemented')
        return results_dict


def load_list_of_stat():
     path = os.getcwd() + '/Statistics/Metrics'
     onlyfiles = [f.split('.')[0] for f in listdir(path) if isfile(join(path, f))]
     path += '/PerformanceMetrics'
     onlyfiles += [f.split('.')[0] for f in listdir(path) if isfile(join(path, f))]

     return onlyfiles

def is_avalible(selected, fullList):
#Check if input module names exist
     sel = selected.split(',')
     for s in sel:
         s = s.strip()
         if s not in fullList:
             corr_input = False
             while(corr_input == False):
                inp = input('Metrics ' + s + ' was not found.\nWould you like to proceed? Y/N')
                if inp.lower() == 'y':
                   sel.remove(s)
                   corr_input = True
                elif inp.lower() == 'n':
                   return list()
     return sel

def import_stats( to_import):
     sel_modules = list()
     for n in to_import:
       try:
         name = 'Statistics.Metrics.' + n.strip()
         module = importlib.import_module(name)
         my_class = getattr(module, n.strip())
         module = my_class()
         sel_modules.append(module)
       except TypeError:
           print('Metric is not correctly implemented')
       except  ModuleNotFoundError:
           print('Module doesnt exist in package Metrics')
       pass
     return sel_modules

def get_total_comission(transactions):

        total_comission = 0
        for transaction in transactions:
            total_comission += transaction.commission

        return total_comission

