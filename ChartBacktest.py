import pandas as pd

import loadData
import sys
from RunStrategy.StartegyGrid import StartegyGrid, single_strategy
from SelectStrategy import SelectStrategy
from Statistics.CalculateStatistic import CalculateStatistic
import save_to_file

if __name__ == "__main__":
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
