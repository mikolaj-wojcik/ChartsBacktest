import pandas as pd

import loadData
import sys

from RequestModels import StrategyModel, StrategyToRunModel
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
import ValidateStrategy

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
@app.post("/validate_strategy")
def validate_strategy(strategy: StrategyModel):
    try:
        # Decode with error handling
        try:
            encoded = strategy.strategy_code.strip()

            # Fix padding
            missing_padding = len(encoded) % 4
            if missing_padding:
                encoded += '=' * (4 - missing_padding)

            decoded_bytes = base64.b64decode(encoded)
            decoded_code = decoded_bytes.decode('utf-8')

        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Base64 decode error: {str(e)}"
            )

        # Load strategy
        lo = StrategyLoader()
        li_code, li_message = lo.load_from_string(decoded_code, strategy.strategy_name)

        if li_code != 0:
            return {"valid": False, "message": li_message}

        # Validate
        val = ValidateStrategy.ValidateStrategy()
        err_list = val.validate(li_message)

        if len(err_list) > 0:
            return {"valid": False, "errors": err_list}

        return {"valid": True, "message": li_message.paramsDict}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/run_strategy")
def run_strategy(strategy : StrategyToRunModel):
    pricesdf = pd.dataframe([p.dict() for p in strategy.prices])
    decoded_bytes = base64.b64decode(strategy.strategy_code)
    decoded_code = decoded_bytes.decode('utf-8')
    lo = StrategyLoader()
    li_code, li_message = lo.load_from_string(decoded_code, strategy.strategy_name)
    if li_code != 0:
       return li_message
    else:
        val = ValidateStrategy.ValidateStrategy()
        err_list = val.validate(li_message)
        if len(err_list) > 0:
            return err_list
    strategy_obj = li_message
    if not ValidateStrategy.validate_parmsDict(strategy_obj.paramsDict, strategy.params):
        return {"valid": False, "errors": "Params not correctly defined"}


    strategy_grid = StartegyGrid(strategy_obj, pricesdf, strategy.starting_balance, strategy.min_commission, strategy.commission_factor, strategy.params)
    strategy_grid.setGrid()
    strategy_grid.runGrid()







if __name__ == "__main__":

    #if
    #GetParamsDictOfStrategy(SelectStrategy(name))
    #strat = StrategyModel
    #strat.strategy_name = 'TestStrategy'
    #strat.strategy_code = 'aW1wb3J0IHBhbmRhcyBhcyBwZAppbXBvcnQgU3RyYXRlZ2llcy5TdHJhdGVneSBhcyBzdHJhdApmcm9tIHRhLnRyZW5kIGltcG9ydCBTTUFJbmRpY2F0b3IKCmNsYXNzIFRlc3RTdHJhdGVneShzdHJhdC5TdHJhdGVneSk6CiAgICBwYXJhbXNEaWN0ID0geydwZXJpb2QnOiAwfQoKICAgIGRlZiBfX2luaXRfXyhzZWxmLCBwcmljZXM9Tm9uZSwgaW5kaWNhdG9yc1BhcmFtcz17J3BlcmlvZCc6IDEwfSk6CiAgICAgICAgc3VwZXIoKS5fX2luaXRfXyhwcmljZXM9cHJpY2VzKQogICAgICAgIHNlbGYuaW5kaWNhdG9yc1BhcmFtcyA9IGluZGljYXRvcnNQYXJhbXMKICAgICAgICBpZiBwcmljZXMgaXMgbm90IE5vbmU6CiAgICAgICAgICAgIHNlbGYuY2FsY3VsYXRlSW5kaWNhdG9ycygpCgogICAgZGVmIHNldFBhcmFtcyhzZWxmLCBwYXJhbXMpOgogICAgICAgIHNlbGYuaW5kaWNhdG9yc1BhcmFtcyA9IHBhcmFtcwogICAgICAgIGlmIG5vdCBzZWxmLnByaWNlcy5lbXB0eToKICAgICAgICAgICAgc2VsZi5jYWxjdWxhdGVJbmRpY2F0b3JzKCkKCiAgICBkZWYgY2FsY3VsYXRlSW5kaWNhdG9ycyhzZWxmKToKICAgICAgICBzbWEgPSBTTUFJbmRpY2F0b3Ioc2VsZi5wcmljZXNbJ2Nsb3NlJ10sIHNlbGYuaW5kaWNhdG9yc1BhcmFtc1sncGVyaW9kJ10pCiAgICAgICAgc2VsZi5wcmljZXNbJ1NNQSddID0gc21hLnNtYV9pbmRpY2F0b3IoKQoKICAgIGRlZiBsb2FkUHJpY2VzKHNlbGYsIHByaWNlcyk6CiAgICAgICAgc3VwZXIoKS5zZXRQcmljZXMocHJpY2VzKQogICAgICAgIHNlbGYuY2FsY3VsYXRlSW5kaWNhdG9ycygpCgogICAgZGVmIG9uVGljayhzZWxmLCBpdGVyKToKICAgICAgICByZXR1cm4gc3VwZXIoKS5vblRpY2soaXRlcik='
    #validate_strategy(strat)
    #SelectStrategy({'class_name': 'TestStrategy', 'code' : TEST_STRAT})
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


