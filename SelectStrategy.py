from Strategies.SMAcross import SMAcross
import importlib


def    SelectStrategy(select):
    module=0
    if(select):
            try:
                name = input('Strategy module name: ')
                classN = input('Strategy module name: ')
                name = 'Strategies.' + name
                module = importlib.import_module(name)
                my_class = getattr(module, classN)
                module = my_class()
            except TypeError:
                 print('Strategy is not correctly implemented')
            except  ModuleNotFoundError:
                 print('Module doesnt exist in package Strategies')
        
        
    else:
        module = SMAcross()
        pass
    return module