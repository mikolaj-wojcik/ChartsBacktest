import pandas as pd
import json
def load_csv(CSVpath):
    try:
        data = pd.read_csv(CSVpath)
        data.columns = ['date', 'open','high','low','close','vol' ]
        return data #pricesStruct.generatePriceListFromDf(data)
    except FileNotFoundError:
        print(f"File {CSVpath} not found")
        return -1

def load_config(filename):
    try:
        with open(filename) as f:
            data = json.load(f)
            required_keys = ["strategy_name", "commission_factor", "min_commission", "csv_output", "starting_balance", "prices_csv", "additional_metrics"]
            if type(data) != list:
                data1 = list()
                data1.append(data)
                data = data1
            for dat in data:
                for key in required_keys:
                    if key not in dat.keys():
                        print(f"Missing parameter {key} in json file")
                        return {}

            return data
    except FileNotFoundError:
        print(f"File {filename} not found")
        return {}
    except json.decoder.JSONDecodeError:
        print(f"Incorrect JSON format in file {filename}")
        return {}
