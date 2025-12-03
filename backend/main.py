import pandas as pd

import loadData
import sys
from dictionaries.priceType import sample_prices
from RequestModels import StrategyModel, StrategyToRunModel
from RunStrategy.StartegyGrid import StartegyGrid, single_strategy
from SelectStrategy import SelectStrategy, StrategyLoader, GetParamsDictOfStrategy
from Statistics.CalculateStatistic import CalculateStatistic, load_list_of_stat
import save_to_file
import RequestModels

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import base64
import ast
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
def get_metrics():
 #   SelectStrategy(name.strategy_name)
    return load_list_of_stat()

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
def run_strategy(passed_strategy : StrategyToRunModel):
    prices_list = [price.model_dump() for price in passed_strategy.prices]
    pricesdf = pd.DataFrame(prices_list)
    startegy_to_init = passed_strategy.strategy_name
    statistics = CalculateStatistic()
    statistics.select_stats(passed_strategy.metrics)
    if passed_strategy.strategy_code != '':
        try:
            # Decode with error handling
            try:
                encoded = passed_strategy.strategy_code.strip()

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
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        startegy_to_init = {"code": decoded_code, "class_name": passed_strategy.strategy_name }
    li_code, li_message = SelectStrategy(startegy_to_init)
    if li_code != 0:
       return li_message
    else:
        val = ValidateStrategy.ValidateStrategy()
        err_list = val.validate(li_message)
        if len(err_list) > 0:
            return err_list
    strategy_obj = li_message
    params_tup = {}
    for key, value in passed_strategy.params.items():
        params_tup[key] = ast.literal_eval(value)
    passed_strategy.params = params_tup
    if not ValidateStrategy.validate_parmsDict(strategy_obj.paramsDict, passed_strategy.params):
        return {"valid": False, "errors": "Params not correctly defined"}


    strategy_grid = StartegyGrid(strategy_obj, pricesdf, passed_strategy.starting_balance, passed_strategy.min_commission, passed_strategy.commission_factor, passed_strategy.params)
    strategy_grid.setGrid()
    result_list = strategy_grid.runGrid()

    for strategy_result in result_list:
        strategy_result.setStatistics(statistics.calculate_performance(strategy_result.prices, transactions=strategy_result.transaction_history, balance=strategy_result.balance, starting_balance=passed_strategy.starting_balance))

    print(result_list)
    return 0






if __name__ == "__main__":


    SelectStrategy({'class_name': 'TestStrategy', 'code' : TEST_STRAT})
    uvicorn.run(app, host="0.0.0.0", port=8000)
    pass

    json_raw = '{"strategy_name":"SMAcross","strategy_code":"","prices":[{"date":"2024-08-19","open":164.872,"high":166.278,"low":163.854,"close":166.258,"volume":22471654},{"date":"2024-08-20","open":166.488,"high":168.224,"low":166.408,"close":166.767,"volume":18386920},{"date":"2024-08-21","open":164.742,"high":166.438,"low":164.264,"close":165.44,"volume":22958669},{"date":"2024-08-22","open":166.847,"high":167.176,"low":162.907,"close":163.396,"volume":22548935},{"date":"2024-08-23","open":164.314,"high":165.77,"low":163.426,"close":165.212,"volume":13990275},{"date":"2024-08-26","open":165.97,"high":167.136,"low":164.049,"close":165.75,"volume":14225531},{"date":"2024-08-27","open":165.425,"high":166.032,"low":164.054,"close":164.274,"volume":11851194},{"date":"2024-08-28","open":164.627,"high":165.192,"low":161.129,"close":162.448,"volume":16448045},{"date":"2024-08-29","open":163.904,"high":165.56,"low":159.855,"close":161.381,"volume":19748515},{"date":"2024-08-30","open":162.214,"high":163.256,"low":161.293,"close":162.976,"volume":22178557},{"date":"2024-09-03","open":161.321,"high":161.451,"low":156.094,"close":156.971,"volume":39041673},{"date":"2024-09-04","open":156.268,"high":158.607,"low":155.577,"close":156.064,"volume":19401650},{"date":"2024-09-05","open":155.914,"high":159.057,"low":155.596,"close":156.852,"volume":18734993},{"date":"2024-09-06","open":156.912,"high":157.441,"low":150.178,"close":150.547,"volume":38005945},{"date":"2024-09-09","open":152.335,"high":153.224,"low":147.046,"close":148.54,"volume":39305446},{"date":"2024-09-10","open":150.278,"high":151.097,"low":148.17,"close":148.49,"volume":31154429},{"date":"2024-09-11","open":149.748,"high":151.327,"low":147.351,"close":150.987,"volume":29641625},{"date":"2024-09-12","open":153.624,"high":154.643,"low":152.475,"close":154.513,"volume":29729080},{"date":"2024-09-13","open":155.252,"high":158.199,"low":155.032,"close":157.28,"volume":29625065},{"date":"2024-09-16","open":157.13,"high":158.069,"low":156.421,"close":157.879,"volume":18400839},{"date":"2024-09-17","open":158.838,"high":160.366,"low":158.194,"close":159.138,"volume":20739353},{"date":"2024-09-18","open":159.677,"high":160.316,"low":158.413,"close":159.627,"volume":23704450},{"date":"2024-09-19","open":163.523,"high":163.603,"low":161.155,"close":161.954,"volume":26618204},{"date":"2024-09-20","open":163.313,"high":163.543,"low":161.874,"close":163.403,"volume":40943308},{"date":"2024-09-23","open":164.162,"high":165.301,"low":161.485,"close":161.665,"volume":24178530},{"date":"2024-09-24","open":162.843,"high":163.029,"low":160.506,"close":162.104,"volume":23358887},{"date":"2024-09-25","open":161.285,"high":162.624,"low":161.115,"close":161.305,"volume":18890824},{"date":"2024-09-26","open":163.453,"high":163.892,"low":162.094,"close":162.544,"volume":20342623},{"date":"2024-09-27","open":162.624,"high":165.51,"low":162.44,"close":163.762,"volume":21125490},{"date":"2024-09-30","open":163.133,"high":165.96,"low":163.073,"close":165.66,"volume":20504775},{"date":"2024-10-01","open":167.493,"high":168.966,"low":164.392,"close":166.799,"volume":28370600},{"date":"2024-10-02","open":166.229,"high":167.328,"low":164.541,"close":165.67,"volume":17780533},{"date":"2024-10-03","open":164.222,"high":166.449,"low":163.735,"close":165.67,"volume":15090375},{"date":"2024-10-04","open":167.868,"high":168.037,"low":165.291,"close":166.869,"volume":19115606},{"date":"2024-10-07","open":167.528,"high":168.287,"low":162.564,"close":162.793,"volume":22488884},{"date":"2024-10-08","open":163.752,"high":164.536,"low":162.684,"close":164.192,"volume":23099175},{"date":"2024-10-09","open":163.263,"high":164.651,"low":159.557,"close":161.675,"volume":31217510},{"date":"2024-10-10","open":160.686,"high":162.883,"low":160.211,"close":161.894,"volume":14160278},{"date":"2024-10-11","open":161.944,"high":163.712,"low":161.05,"close":163.053,"volume":15361836},{"date":"2024-10-14","open":163.453,"high":166.036,"low":163.213,"close":164.771,"volume":19037934},{"date":"2024-10-15","open":165.595,"high":167.488,"low":164.437,"close":165.271,"volume":20270399},{"date":"2024-10-16","open":164.342,"high":165.61,"low":163.553,"close":164.971,"volume":16424832},{"date":"2024-10-17","open":165.54,"high":166.18,"low":162.574,"close":162.743,"volume":21477982},{"date":"2024-10-18","open":163.003,"high":164.521,"low":162.893,"close":163.233,"volume":19780304},{"date":"2024-10-21","open":162.763,"high":164.312,"low":162.434,"close":163.882,"volume":20970461},{"date":"2024-10-22","open":162.793,"high":165.58,"low":162.793,"close":164.951,"volume":16587109},{"date":"2024-10-23","open":164.571,"high":165.63,"low":161.74,"close":162.594,"volume":18301468},{"date":"2024-10-24","open":162.644,"high":163.143,"low":160.826,"close":162.534,"volume":22438213},{"date":"2024-10-25","open":163.483,"high":165.4,"low":163.233,"close":165.081,"volume":19851609},{"date":"2024-10-28","open":168.557,"high":168.557,"low":163.762,"close":166.529,"volume":32175474},{"date":"2024-10-29","open":167.538,"high":170.185,"low":166.898,"close":169.486,"volume":42217353},{"date":"2024-10-30","open":180.473,"high":181.812,"low":173.861,"close":174.26,"volume":68969740},{"date":"2024-10-31","open":172.932,"high":176.618,"low":170.804,"close":170.914,"volume":44820289},{"date":"2024-11-01","open":169.875,"high":172.123,"low":168.687,"close":171.094,"volume":31832917},{"date":"2024-11-04","open":169.735,"high":170.535,"low":167.819,"close":169.046,"volume":21517376},{"date":"2024-11-05","open":169.236,"high":170.335,"low":168.647,"close":169.546,"volume":18262956},{"date":"2024-11-06","open":173.601,"high":176.737,"low":173.301,"close":176.308,"volume":33734155},{"date":"2024-11-07","open":177.207,"high":180.873,"low":176.987,"close":180.543,"volume":25381995},{"date":"2024-11-08","open":180.438,"high":180.693,"low":177.876,"close":178.146,"volume":22031402},{"date":"2024-11-11","open":178.376,"high":180.338,"low":178.266,"close":180.144,"volume":17470353},{"date":"2024-11-12","open":179.614,"high":182.281,"low":179.185,"close":181.412,"volume":25163711},{"date":"2024-11-13","open":180.253,"high":180.753,"low":178.336,"close":178.675,"volume":23210573},{"date":"2024-11-14","open":178.076,"high":178.615,"low":174.122,"close":175.379,"volume":31042993},{"date":"2024-11-15","open":173.531,"high":173.941,"low":171.024,"close":172.293,"volume":32541901},{"date":"2024-11-18","open":173.221,"high":175.237,"low":172.702,"close":175.099,"volume":20229771},{"date":"2024-11-19","open":173.521,"high":178.665,"low":173.361,"close":177.916,"volume":23461782},{"date":"2024-11-20","open":177.137,"high":177.472,"low":173.581,"close":175.779,"volume":19018882},{"date":"2024-11-21","open":173.701,"high":173.931,"low":163.513,"close":167.438,"volume":59802838},{"date":"2024-11-22","open":165.66,"high":166.269,"low":163.712,"close":164.571,"volume":38648830},{"date":"2024-11-25","open":165.9,"high":168.437,"low":165.418,"close":167.458,"volume":33173238},{"date":"2024-11-26","open":167.438,"high":169.626,"low":167.388,"close":168.926,"volume":20510199},{"date":"2024-11-27","open":168.807,"high":169.289,"low":167.828,"close":169.036,"volume":19288591},{"date":"2024-11-29","open":168.307,"high":169.236,"low":166.969,"close":168.757,"volume":14273583},{"date":"2024-12-02","open":168.572,"high":171.878,"low":168.377,"close":171.294,"volume":23816347},{"date":"2024-12-03","open":171.294,"high":172.482,"low":170.654,"close":171.144,"volume":22274203},{"date":"2024-12-04","open":170.949,"high":174.71,"low":170.864,"close":174.17,"volume":31651370},{"date":"2024-12-05","open":175.159,"high":175.858,"low":172.133,"close":172.442,"volume":21380718},{"date":"2024-12-06","open":171.833,"high":174.88,"low":171.663,"close":174.51,"volume":21486990},{"date":"2024-12-09","open":173.96,"high":176.26,"low":173.65,"close":175.37,"volume":25389631},{"date":"2024-12-10","open":182.845,"high":186.36,"low":181.05,"close":185.17,"volume":54813022},{"date":"2024-12-11","open":185.31,"high":195.61,"low":184.85,"close":195.4,"volume":67894071},{"date":"2024-12-12","open":195,"high":195.18,"low":191.71,"close":191.96,"volume":34817486},{"date":"2024-12-13","open":191.01,"high":192.73,"low":189.64,"close":189.82,"volume":25143495},{"date":"2024-12-16","open":192.87,"high":199,"low":192.62,"close":196.66,"volume":44934901},{"date":"2024-12-17","open":197.25,"high":201.42,"low":194.98,"close":195.42,"volume":43504025},{"date":"2024-12-18","open":195.22,"high":197,"low":187.74,"close":188.4,"volume":34166074},{"date":"2024-12-19","open":191.625,"high":193.03,"low":188.38,"close":188.51,"volume":32265241},{"date":"2024-12-20","open":185.78,"high":192.89,"low":185.22,"close":191.41,"volume":63462934},{"date":"2024-12-23","open":192.62,"high":195.1,"low":190.15,"close":194.63,"volume":25675014},{"date":"2024-12-24","open":194.84,"high":196.11,"low":193.78,"close":196.11,"volume":10403259},{"date":"2024-12-26","open":195.15,"high":196.748,"low":194.375,"close":195.6,"volume":12057210},{"date":"2024-12-27","open":194.95,"high":195.32,"low":190.65,"close":192.76,"volume":18891362},{"date":"2024-12-30","open":189.8,"high":192.55,"low":189.12,"close":191.24,"volume":14264659},{"date":"2024-12-31","open":191.075,"high":191.96,"low":188.51,"close":189.3,"volume":17466919},{"date":"2025-01-02","open":190.65,"high":192,"low":187.5,"close":189.43,"volume":20370828},{"date":"2025-01-03","open":191.37,"high":193.21,"low":189.975,"close":191.79,"volume":18596159},{"date":"2025-01-06","open":193.98,"high":198.222,"low":193.85,"close":196.87,"volume":29563638},{"date":"2025-01-07","open":197.11,"high":201,"low":194.6,"close":195.49,"volume":26487244},{"date":"2025-01-08","open":192.57,"high":196.29,"low":192.38,"close":193.95,"volume":24864766},{"date":"2025-01-10","open":194.295,"high":196.52,"low":190.31,"close":192.04,"volume":26665206},{"date":"2025-01-13","open":190.07,"high":191.18,"low":187.36,"close":191.01,"volume":21823699},{"date":"2025-01-14","open":191.24,"high":191.98,"low":188.308,"close":189.66,"volume":17174854},{"date":"2025-01-15","open":193.09,"high":196.36,"low":191.86,"close":195.55,"volume":21775969},{"date":"2025-01-16","open":194.14,"high":195.48,"low":192.81,"close":192.91,"volume":17815432},{"date":"2025-01-17","open":196.53,"high":197.23,"low":193.75,"close":196,"volume":27735089},{"date":"2025-01-21","open":198.985,"high":202.29,"low":197.87,"close":198.05,"volume":29971292},{"date":"2025-01-22","open":199.06,"high":200.48,"low":197.53,"close":198.37,"volume":26200617},{"date":"2025-01-23","open":198.14,"high":200.3,"low":195.2,"close":197.98,"volume":26951357},{"date":"2025-01-24","open":198.1,"high":200.9,"low":198,"close":200.21,"volume":23877521},{"date":"2025-01-27","open":192.41,"high":196.88,"low":190.73,"close":191.81,"volume":41728893},{"date":"2025-01-28","open":192.745,"high":195.48,"low":190.68,"close":195.3,"volume":24157929},{"date":"2025-01-29","open":195.555,"high":196.785,"low":193.43,"close":195.41,"volume":18218256},{"date":"2025-01-30","open":198,"high":201.4,"low":197.67,"close":200.87,"volume":24354684},{"date":"2025-01-31","open":202,"high":205.48,"low":201.8,"close":204.02,"volume":32041952},{"date":"2025-02-03","open":200.69,"high":203.75,"low":200.1,"close":201.23,"volume":27838348},{"date":"2025-02-04","open":203.39,"high":207.05,"low":202.81,"close":206.38,"volume":43856425},{"date":"2025-02-05","open":191.07,"high":192.75,"low":188.03,"close":191.33,"volume":70461770},{"date":"2025-02-06","open":189.5,"high":192.1,"low":188.72,"close":191.6,"volume":29297442},{"date":"2025-02-07","open":191.05,"high":191.18,"low":183.24,"close":185.34,"volume":49314961},{"date":"2025-02-10","open":187.35,"high":188.2,"low":185.86,"close":186.47,"volume":23105649},{"date":"2025-02-11","open":185.03,"high":186.94,"low":184.28,"close":185.32,"volume":21239519},{"date":"2025-02-12","open":183.22,"high":185.11,"low":181.83,"close":183.61,"volume":22072559},{"date":"2025-02-13","open":184.32,"high":186.28,"low":183.14,"close":186.14,"volume":21402523},{"date":"2025-02-14","open":185.055,"high":186.4,"low":184.32,"close":185.23,"volume":20448437},{"date":"2025-02-18","open":185.6,"high":185.96,"low":181.74,"close":183.77,"volume":29916675},{"date":"2025-02-19","open":184.07,"high":185.46,"low":183.59,"close":185.27,"volume":19549396},{"date":"2025-02-20","open":184.8,"high":185.31,"low":182.72,"close":184.56,"volume":20441462},{"date":"2025-02-21","open":185.15,"high":185.34,"low":179.08,"close":179.66,"volume":35199239},{"date":"2025-02-24","open":182.05,"high":183.12,"low":178.885,"close":179.32,"volume":29854206},{"date":"2025-02-25","open":178.04,"high":178.74,"low":174.693,"close":175.42,"volume":41913411},{"date":"2025-02-26","open":175.07,"high":176.08,"low":171.58,"close":172.73,"volume":35431268},{"date":"2025-02-27","open":173.99,"high":174.56,"low":167.94,"close":168.5,"volume":39991015},{"date":"2025-02-28","open":168.68,"high":170.61,"low":166.77,"close":170.28,"volume":48130565},{"date":"2025-03-03","open":171.925,"high":173.37,"low":165.93,"close":167.01,"volume":40770451},{"date":"2025-03-04","open":166.24,"high":173.2946,"low":165.8,"close":170.92,"volume":45387996},{"date":"2025-03-05","open":170.52,"high":173.78,"low":169.06,"close":173.02,"volume":30954922},{"date":"2025-03-06","open":170.53,"high":174.81,"low":170.5,"close":172.35,"volume":28301953},{"date":"2025-03-07","open":171.26,"high":174.97,"low":170.27,"close":173.86,"volume":27385813},{"date":"2025-03-10","open":168.26,"high":168.46,"low":163.69,"close":165.87,"volume":43604027},{"date":"2025-03-11","open":164.91,"high":166.75,"low":161.37,"close":164.04,"volume":39587414},{"date":"2025-03-12","open":166.58,"high":167.6399,"low":163.53,"close":167.11,"volume":28372396},{"date":"2025-03-13","open":166.035,"high":166.13,"low":162.11,"close":162.76,"volume":31756214},{"date":"2025-03-14","open":163.27,"high":166.49,"low":162.45,"close":165.49,"volume":31995894},{"date":"2025-03-17","open":165.03,"high":166.3,"low":163.67,"close":164.29,"volume":31184335},{"date":"2025-03-18","open":163.675,"high":164.25,"low":156.72,"close":160.67,"volume":42074751},{"date":"2025-03-19","open":161.76,"high":165.87,"low":161,"close":163.89,"volume":34275582},{"date":"2025-03-20","open":161.57,"high":164.89,"low":160.96,"close":162.8,"volume":28138464},{"date":"2025-03-21","open":161.205,"high":164.24,"low":160.8901,"close":163.99,"volume":36625764},{"date":"2025-03-24","open":167.065,"high":168.32,"low":165.14,"close":167.68,"volume":30879129},{"date":"2025-03-25","open":168.98,"high":170.63,"low":168.315,"close":170.56,"volume":24174373},{"date":"2025-03-26","open":169,"high":169.61,"low":164.84,"close":165.06,"volume":28939326},{"date":"2025-03-27","open":164.63,"high":165.42,"low":162,"close":162.24,"volume":24508273},{"date":"2025-03-28","open":160.49,"high":161.82,"low":153.63,"close":154.33,"volume":48669335},{"date":"2025-03-31","open":153.11,"high":155.54,"low":150.662,"close":154.64,"volume":54603464},{"date":"2025-04-01","open":153.62,"high":158.1,"low":153.62,"close":157.07,"volume":30672899},{"date":"2025-04-02","open":155.15,"high":158.4052,"low":154.7,"close":157.04,"volume":25041730},{"date":"2025-04-03","open":151.11,"high":152.7799,"low":150.39,"close":150.72,"volume":46883371},{"date":"2025-04-04","open":148.01,"high":151.07,"low":145.38,"close":145.6,"volume":62259539},{"date":"2025-04-07","open":141.55,"high":152.85,"low":140.53,"close":146.75,"volume":76794136},{"date":"2025-04-08","open":151.22,"high":152.24,"low":143.03,"close":144.7,"volume":52200208},{"date":"2025-04-09","open":144.415,"high":159.55,"low":143.905,"close":158.71,"volume":70406232},{"date":"2025-04-10","open":156.54,"high":157.72,"low":149.93,"close":152.82,"volume":48021972},{"date":"2025-04-11","open":152.9,"high":157.67,"low":152.82,"close":157.14,"volume":33636239},{"date":"2025-04-14","open":159.995,"high":161.72,"low":157.56,"close":159.07,"volume":30332957},{"date":"2025-04-15","open":159.125,"high":159.65,"low":155.21,"close":156.31,"volume":27551534},{"date":"2025-04-16","open":153.1,"high":155.89,"low":151.51,"close":153.33,"volume":28187421},{"date":"2025-04-17","open":154.29,"high":154.68,"low":148.5,"close":151.16,"volume":33046576},{"date":"2025-04-21","open":148.88,"high":148.945,"low":146.1,"close":147.67,"volume":26049115},{"date":"2025-04-22","open":148.89,"high":152.19,"low":148.54,"close":151.47,"volume":26971774},{"date":"2025-04-23","open":155.61,"high":157.525,"low":153.81,"close":155.35,"volume":31128833},{"date":"2025-04-24","open":156.15,"high":159.59,"low":155.79,"close":159.28,"volume":45893951},{"date":"2025-04-25","open":165.07,"high":166.1,"low":161.04,"close":161.96,"volume":56033995},{"date":"2025-04-28","open":162.425,"high":163.15,"low":158.6,"close":160.61,"volume":29745782},{"date":"2025-04-29","open":160.325,"high":160.74,"low":157.52,"close":160.16,"volume":26808958},{"date":"2025-04-30","open":157.975,"high":159.27,"low":155.4,"close":158.8,"volume":34981059},{"date":"2025-05-01","open":160.45,"high":161.95,"low":158.91,"close":161.3,"volume":30203248},{"date":"2025-05-02","open":163.405,"high":164.97,"low":161.87,"close":164.03,"volume":25715005},{"date":"2025-05-05","open":163,"high":165.39,"low":162.72,"close":164.21,"volume":21341814},{"date":"2025-05-06","open":162.17,"high":164.8,"low":161.19,"close":163.23,"volume":21277210},{"date":"2025-05-07","open":164.08,"high":165,"low":147.84,"close":151.38,"volume":127747554},{"date":"2025-05-08","open":155,"high":155.93,"low":152.9,"close":154.28,"volume":57498692},{"date":"2025-05-09","open":154.17,"high":155.05,"low":152.2,"close":152.75,"volume":32435281},{"date":"2025-05-12","open":157.485,"high":159.1,"low":156.25,"close":158.46,"volume":44138818},{"date":"2025-05-13","open":158.79,"high":160.57,"low":156.16,"close":159.53,"volume":42382126},{"date":"2025-05-14","open":159.96,"high":167,"low":159.61,"close":165.37,"volume":48755869},{"date":"2025-05-15","open":165.84,"high":166.205,"low":162.3732,"close":163.96,"volume":33146669},{"date":"2025-05-16","open":167.725,"high":169.35,"low":165.62,"close":166.19,"volume":42846925},{"date":"2025-05-19","open":164.51,"high":166.64,"low":164.22,"close":166.54,"volume":30426097},{"date":"2025-05-20","open":166.43,"high":168.5,"low":162.9,"close":163.98,"volume":46607656},{"date":"2025-05-21","open":163.69,"high":173.14,"low":163.56,"close":168.56,"volume":73415956},{"date":"2025-05-22","open":171.85,"high":176.77,"low":170.71,"close":170.87,"volume":74864418},{"date":"2025-05-23","open":169.055,"high":169.96,"low":167.89,"close":168.47,"volume":35211439},{"date":"2025-05-27","open":170.16,"high":173.17,"low":170,"close":172.9,"volume":37995670},{"date":"2025-05-28","open":173.16,"high":175.265,"low":171.9107,"close":172.36,"volume":34783997},{"date":"2025-05-29","open":174,"high":174.4193,"low":170.63,"close":171.86,"volume":29373803},{"date":"2025-05-30","open":171.35,"high":172.205,"low":167.44,"close":171.74,"volume":52639911},{"date":"2025-06-02","open":167.84,"high":169.87,"low":167.39,"close":169.03,"volume":38612272},{"date":"2025-06-03","open":167.49,"high":168.475,"low":165.28,"close":166.18,"volume":45084903},{"date":"2025-06-04","open":166.735,"high":168.215,"low":166.36,"close":168.05,"volume":26900838},{"date":"2025-06-05","open":170.34,"high":170.93,"low":167.59,"close":168.21,"volume":36444564},{"date":"2025-06-06","open":170.83,"high":174.5,"low":170.83,"close":173.68,"volume":35731832},{"date":"2025-06-09","open":174.54,"high":176.47,"low":174.37,"close":176.09,"volume":28935906},{"date":"2025-06-10","open":176.2,"high":181.105,"low":174.91,"close":178.6,"volume":61766121},{"date":"2025-06-11","open":179.77,"high":180.37,"low":176.75,"close":177.35,"volume":31646757},{"date":"2025-06-12","open":176.18,"high":176.72,"low":174.745,"close":175.7,"volume":20941873},{"date":"2025-06-13","open":172.44,"high":177.13,"low":172.385,"close":174.67,"volume":27663107},{"date":"2025-06-16","open":174.73,"high":176.94,"low":174.65,"close":176.77,"volume":27389208},{"date":"2025-06-17","open":175.7,"high":177.3648,"low":174.58,"close":175.95,"volume":24973043},{"date":"2025-06-18","open":176.01,"high":176.56,"low":173.2,"close":173.32,"volume":28707524},{"date":"2025-06-20","open":173.945,"high":174.34,"low":165.46,"close":166.64,"volume":75659917},{"date":"2025-06-23","open":166.27,"high":167.34,"low":162,"close":165.19,"volume":57670985},{"date":"2025-06-24","open":166.92,"high":168.22,"low":166.13,"close":166.77,"volume":40524312},{"date":"2025-06-25","open":167.63,"high":172.36,"low":167.55,"close":170.68,"volume":35478989},{"date":"2025-06-26","open":172.43,"high":173.69,"low":169.94,"close":173.54,"volume":31796690},{"date":"2025-06-27","open":173.54,"high":178.68,"low":171.73,"close":178.53,"volume":108140200},{"date":"2025-06-30","open":180.78,"high":181.23,"low":174.58,"close":176.23,"volume":63378856},{"date":"2025-07-01","open":175.735,"high":176.09,"low":173.53,"close":175.84,"volume":35904526},{"date":"2025-07-02","open":175.54,"high":178.86,"low":175.07,"close":178.64,"volume":29128947},{"date":"2025-07-03","open":178.5,"high":179.67,"low":177.05,"close":179.53,"volume":21689729},{"date":"2025-07-07","open":179.06,"high":179.297,"low":175.68,"close":176.79,"volume":34175648},{"date":"2025-07-08","open":177.85,"high":177.95,"low":172.81,"close":174.36,"volume":40442535},{"date":"2025-07-09","open":175.25,"high":179.44,"low":172.77,"close":176.62,"volume":43025594},{"date":"2025-07-10","open":175.63,"high":178.429,"low":174.38,"close":177.62,"volume":29252386},{"date":"2025-07-11","open":176.785,"high":181.43,"low":176.48,"close":180.19,"volume":34282922},{"date":"2025-07-14","open":181.01,"high":183.67,"low":179.68,"close":181.56,"volume":32536632},{"date":"2025-07-15","open":182.81,"high":184.22,"low":181.6,"close":182,"volume":33448251},{"date":"2025-07-16","open":183.235,"high":184.327,"low":182.03,"close":182.97,"volume":33104193},{"date":"2025-07-17","open":182.14,"high":184.06,"low":180.48,"close":183.58,"volume":31992565},{"date":"2025-07-18","open":185.4,"high":186.42,"low":183.71,"close":185.06,"volume":34014509},{"date":"2025-07-21","open":186.25,"high":190.285,"low":186.15,"close":190.1,"volume":45803129},{"date":"2025-07-22","open":191.495,"high":191.645,"low":187.46,"close":191.34,"volume":44660215},{"date":"2025-07-23","open":191.5,"high":192.53,"low":189.18,"close":190.23,"volume":58681948},{"date":"2025-07-24","open":197.03,"high":197.95,"low":191,"close":192.17,"volume":74881687},{"date":"2025-07-25","open":191.98,"high":194.33,"low":191.26,"close":193.18,"volume":39785863},{"date":"2025-07-28","open":193.65,"high":194.05,"low":190.84,"close":192.58,"volume":38139504},{"date":"2025-07-29","open":192.43,"high":195.92,"low":192.08,"close":195.75,"volume":41389153},{"date":"2025-07-30","open":195.6,"high":197.5999,"low":194.685,"close":196.53,"volume":32445405},{"date":"2025-07-31","open":195.71,"high":195.99,"low":191.09,"close":191.9,"volume":51329163},{"date":"2025-08-01","open":189.025,"high":190.83,"low":187.82,"close":189.13,"volume":34832181},{"date":"2025-08-04","open":190.29,"high":195.27,"low":190.12,"close":195.04,"volume":31547350},{"date":"2025-08-05","open":194.71,"high":197.8599,"low":193.885,"close":194.67,"volume":31602340},{"date":"2025-08-06","open":194.5,"high":196.63,"low":193.67,"close":196.09,"volume":21562908},{"date":"2025-08-07","open":197.06,"high":197.54,"low":194.33,"close":196.52,"volume":26321811},{"date":"2025-08-08","open":197.22,"high":202.61,"low":197.17,"close":201.42,"volume":39161826},{"date":"2025-08-11","open":200.935,"high":201.475,"low":199.07,"close":201,"volume":25832435},{"date":"2025-08-12","open":201.365,"high":204.5,"low":200.59,"close":203.34,"volume":30424452},{"date":"2025-08-13","open":204.13,"high":204.53,"low":197.5101,"close":201.96,"volume":28342922},{"date":"2025-08-14","open":201.5,"high":204.44,"low":201.225,"close":202.94,"volume":25230427},{"date":"2025-08-15","open":203.85,"high":206.44,"low":201.28,"close":203.9,"volume":34931422},{"date":"2025-08-18","open":204.2,"high":205.265,"low":202.49,"close":203.5,"volume":18526594},{"date":"2025-08-19","open":203.03,"high":203.44,"low":199.96,"close":201.57,"volume":24240233},{"date":"2025-08-20","open":200.73,"high":201.28,"low":196.595,"close":199.32,"volume":28955498},{"date":"2025-08-21","open":199.745,"high":202.48,"low":199.43,"close":199.75,"volume":19774633},{"date":"2025-08-22","open":202.73,"high":208.54,"low":201.3,"close":206.09,"volume":42827040},{"date":"2025-08-25","open":206.43,"high":210.52,"low":205.28,"close":208.49,"volume":29928878},{"date":"2025-08-26","open":207.51,"high":207.85,"low":205.7,"close":207.14,"volume":28464130},{"date":"2025-08-27","open":205.7,"high":208.91,"low":205.65,"close":207.48,"volume":23022850},{"date":"2025-08-28","open":207.25,"high":212.22,"low":206.9,"close":211.64,"volume":32339307},{"date":"2025-08-29","open":210.51,"high":214.645,"low":210.2,"close":212.91,"volume":39728364},{"date":"2025-09-02","open":208.44,"high":211.675,"low":206.195,"close":211.35,"volume":47523037},{"date":"2025-09-03","open":226.21,"high":231.31,"low":224.79,"close":230.66,"volume":103336125},{"date":"2025-09-04","open":229.65,"high":232.37,"low":226.11,"close":232.3,"volume":51684167},{"date":"2025-09-05","open":232.2,"high":235.76,"low":231.9,"close":235,"volume":46588925},{"date":"2025-09-08","open":235.47,"high":238.13,"low":233.67,"close":234.04,"volume":32474743},{"date":"2025-09-09","open":234.165,"high":240.47,"low":233.229,"close":239.63,"volume":38060959},{"date":"2025-09-10","open":238.9,"high":241.66,"low":237.85,"close":239.17,"volume":35141074},{"date":"2025-09-11","open":239.88,"high":242.25,"low":236.25,"close":240.37,"volume":30599328},{"date":"2025-09-12","open":240.37,"high":242.075,"low":238,"close":240.8,"volume":26771610},{"date":"2025-09-15","open":244.66,"high":252.4099,"low":244.66,"close":251.61,"volume":58383796},{"date":"2025-09-16","open":252.08,"high":253.04,"low":249.47,"close":251.16,"volume":34109720},{"date":"2025-09-17","open":251.22,"high":251.6,"low":246.28,"close":249.53,"volume":34107992},{"date":"2025-09-18","open":251.68,"high":253.99,"low":249.8,"close":252.03,"volume":31239474},{"date":"2025-09-19","open":253.25,"high":256,"low":251.81,"close":254.72,"volume":55571424},{"date":"2025-09-22","open":254.43,"high":255.78,"low":250.3,"close":252.53,"volume":32290538},{"date":"2025-09-23","open":253.04,"high":254.36,"low":250.48,"close":251.66,"volume":26628016},{"date":"2025-09-24","open":251.66,"high":252.3501,"low":246.44,"close":247.14,"volume":28201003},{"date":"2025-09-25","open":244.4,"high":246.49,"low":240.74,"close":245.79,"volume":31020383},{"date":"2025-09-26","open":247.065,"high":249.42,"low":245.97,"close":246.54,"volume":18503194},{"date":"2025-09-29","open":247.85,"high":251.1486,"low":242.77,"close":244.05,"volume":32505777},{"date":"2025-09-30","open":242.81,"high":243.29,"low":239.245,"close":243.1,"volume":34724346},{"date":"2025-10-01","open":240.75,"high":246.3,"low":238.61,"close":244.9,"volume":31658234},{"date":"2025-10-02","open":245.15,"high":246.81,"low":242.3,"close":245.69,"volume":25483298},{"date":"2025-10-03","open":244.49,"high":246.3,"low":241.655,"close":245.35,"volume":30249559},{"date":"2025-10-06","open":244.78,"high":251.32,"low":244.58,"close":250.43,"volume":28894653},{"date":"2025-10-07","open":248.27,"high":250.44,"low":245.52,"close":245.76,"volume":23181285},{"date":"2025-10-08","open":244.96,"high":246.005,"low":243.82,"close":244.62,"volume":21307104},{"date":"2025-10-09","open":244.47,"high":244.76,"low":239.15,"close":241.53,"volume":27892086},{"date":"2025-10-10","open":241.43,"high":244.09,"low":235.84,"close":236.57,"volume":33180323},{"date":"2025-10-13","open":240.21,"high":244.5,"low":239.71,"close":244.15,"volume":24995028},{"date":"2025-10-14","open":241.23,"high":247.12,"low":240.51,"close":245.45,"volume":22111572},{"date":"2025-10-15","open":247.245,"high":252.11,"low":245.99,"close":251.03,"volume":27007690},{"date":"2025-10-16","open":251.765,"high":256.96,"low":250.101,"close":251.46,"volume":27997159},{"date":"2025-10-17","open":250.76,"high":254.22,"low":247.81,"close":253.3,"volume":29671629},{"date":"2025-10-20","open":254.69,"high":257.33,"low":254.23,"close":256.55,"volume":22350155},{"date":"2025-10-21","open":254.74,"high":254.88,"low":244.15,"close":250.46,"volume":47312098},{"date":"2025-10-22","open":254.37,"high":256.36,"low":249.29,"close":251.69,"volume":35029370},{"date":"2025-10-23","open":252.98,"high":255.04,"low":251.85,"close":253.08,"volume":19901425},{"date":"2025-10-24","open":256.58,"high":261.68,"low":255.315,"close":259.92,"volume":28655126},{"date":"2025-10-27","open":264.815,"high":270.14,"low":264.28,"close":269.27,"volume":35235231},{"date":"2025-10-28","open":269.69,"high":270.73,"low":266.5,"close":267.47,"volume":29738564},{"date":"2025-10-29","open":267.75,"high":275.336,"low":267.67,"close":274.57,"volume":43580277},{"date":"2025-10-30","open":291.59,"high":291.59,"low":280.06,"close":281.48,"volume":74875990},{"date":"2025-10-31","open":283.21,"high":286,"low":277.03,"close":281.19,"volume":39267945},{"date":"2025-11-03","open":282.175,"high":285.53,"low":279.8,"close":283.72,"volume":29785996},{"date":"2025-11-04","open":276.75,"high":281.27,"low":276.26,"close":277.54,"volume":30078369},{"date":"2025-11-05","open":278.87,"high":286.415,"low":277.34,"close":284.31,"volume":31010302},{"date":"2025-11-06","open":285.33,"high":288.35,"low":281.14,"close":284.75,"volume":37173648},{"date":"2025-11-07","open":283.205,"high":283.78,"low":275.19,"close":278.83,"volume":34479588},{"date":"2025-11-10","open":284.42,"high":290.8,"low":282.855,"close":290.1,"volume":29557309},{"date":"2025-11-11","open":287.745,"high":291.915,"low":287.32,"close":291.31,"volume":19842136},{"date":"2025-11-12","open":291.675,"high":292.005,"low":283.69,"close":286.71,"volume":24829923},{"date":"2025-11-13","open":282.34,"high":282.84,"low":277.24,"close":278.57,"volume":29494040},{"date":"2025-11-14","open":271.405,"high":278.56,"low":270.7,"close":276.41,"volume":31647227}],"params":{"shortSMA":"(10,15,1)","longSMA":"(20,30,1)"},"starting_balance":2000,"min_commission":10,"commission_factor":0.01,"metrics":["Gross Profit","Gross Loss","Profit Factor"]}'
    user_dict = json.loads(json_raw)
    user = StrategyToRunModel(**user_dict)

    run_strategy(user)
    pass


