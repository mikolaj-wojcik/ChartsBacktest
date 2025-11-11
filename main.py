import pandas as pd

import loadData
import sys

from RequestModels import StrategyModel
from RunStrategy.StartegyGrid import StartegyGrid, single_strategy
from SelectStrategy import SelectStrategy, StrategyLoader, GetParamsDictOfStrategy
from Statistics.CalculateStatistic import CalculateStatistic, load_list_of_stat
import save_to_file
import RequestModels

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import base64
from pydantic import BaseModel
import pandas as pd
import numpy as np
import ast
import json
from typing import List, Dict, Any
import traceback
from datetime import datetime
import io
import uvicorn

from Strategies.SMAcross import SMAcross

TEST_STRAT = """
import pandas as pd
import Strategies.Strategy as strat
from ta.trend import SMAIndicator

class TestStrategy(strat.Strategy):
    paramsDict = {'period': 0}

    def __init__(self, prices=None, indicatorsParams={'period': 10}):
        super().__init__(prices=prices)
        self.indicatorsParams = indicatorsParams
        if prices is not None:
            self.calculateIndicators()

    def setParams(self, params):
        self.indicatorsParams = params
        if not self.prices.empty:
            self.calculateIndicators()

    def calculateIndicators(self):
        sma = SMAIndicator(self.prices['close'], self.indicatorsParams['period'])
        self.prices['SMA'] = sma.sma_indicator()

    def loadPrices(self, prices):
        super().setPrices(prices)
        self.calculateIndicators()

    def onTick(self, iter):
        return super().onTick(iter)
"""

BAD_STRAT = """
import os
class BadStrategy:
    paramsDict = {}
    def onTick(self, iter):
        os.system('rm -rf /')  # Malicious!
        return 0
"""
app = FastAPI(title="Trading Strategy Backtester")

# CORS for Flutter web
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/health2")
def health_check1():
    return {"status": "zdrowy"}

@app.get("/calculate")
def calculate():
    return {"stat":"Baby"}

@app.get("/avalible_default_starts")
def avalible_default_starts():
    return(StrategyLoader().ListDefaultStrategies())

@app.get("/strategy/{str_name}")
def get_params(str_name : str):
 #   SelectStrategy(name.strategy_name)
    code, strategy =  SelectStrategy(str_name)
    if code != 0:
        return strategy
    else:
        return GetParamsDictOfStrategy(strategy)

@app.get("/metrics")
def get_params():
 #   SelectStrategy(name.strategy_name)
    return load_list_of_stat()

@app.post("/validate_strategy")
def validate_strategy(strategy : StrategyModel):
    decoded_bytes = base64.b64decode(strategy.strategy_code)
    decoded_code = decoded_bytes.decode('utf-8')
    lo = StrategyLoader()
    li_code, li_message = lo.load_from_string(decoded_code, strategy.strategy_name)
    if li_code != 0:
       return li_message
    else:
       return 'Valid'
#    #return GetParamsDictOfStrategy(ls_name)


if __name__ == "__main__":
    name = '999'
    #startegy
    #if
    #GetParamsDictOfStrategy(SelectStrategy(name))

    SelectStrategy({'class_name': 'TestStrategy', 'code' : TEST_STRAT})
    uvicorn.run(app, host="0.0.0.0", port=8000)
    pass

    """
    uvicorn.run(app, host="0.0.0.0", port=8000)
    if len(sys.argv) >1:
        filename = sys.argv[1]
        inputParamsDict = loadData.load_config(filename)
        if len(inputParamsDict) == 0:

            pass
            #skip
        for single in inputParamsDict:
            prices = loadData.load_csv(single["prices_csv"])
            if type(prices) == pd.DataFrame:
                strat = SelectStrategy(single["strategy_name"])
                if(strat != 0):
                    starting_balance = single["starting_balance"]
                    grid = StartegyGrid(strat, prices, starting_balance= starting_balance, min_commission=single["min_commission"], commission_factor=single["commission_factor"], strategy_params = (single['params'] if 'params' in single.keys() else {}))
                    if grid.setGrid() == 0:
                        print("Calculating...")
                        list_strat = grid.runGrid()
                        statistics = CalculateStatistic()
                        statistics.select_stats(single["additional_metrics"])
                        stats_and_plots = []
                        for strat in list_strat:
                            strat.setStatistics(statistics.calculate_performance(strat.prices, transactions=strat.transaction_history, balance= strat.balance, starting_balance = starting_balance))
                            #strat struct: name(dict) (prices etc.) (statiscts dict)
                            #strat
                        print("Generating document...")
                        save_to_file.save_to_file_csv(list_strat, single["csv_output"])
                        save_to_file.save_to_file_latex(list_strat, stats_and_plots,prices, (single['pdf_path'] if 'pdf_path' in single.keys() else ''))
    else:
        print('Please provide correct JSON file with configuration.')
    """


