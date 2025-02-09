from Strategies.SMAcross import SMAcross
import importlib
import os


def SelectStrategy(strategy_name):
    module=0
    if(strategy_name):
            try:
               # name = input('Strategy module name: ')
                strategy_name_w = 'Strategies.' + strategy_name
                module = importlib.import_module(strategy_name_w)
                my_class = getattr(module, strategy_name)
                module = my_class()
            except TypeError:
                 print('Strategy is not correctly implemented')
            except  ModuleNotFoundError:
                 print('Module ' + strategy_name+ ' doesnt exist in package Strategies')
            except AttributeError:
                print('There is no strategy called ' + strategy_name + 'in module Strategies')

    else:
       module = SMAcross()
       pass
    return module