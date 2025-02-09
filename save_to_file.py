from matplotlib.backends.backend_pdf import PdfPages
import Charts.chartcreator as chart
import shutil
import os
import pandas as pd
from pylatex import (
    Alignat,
    Axis,
    Document,
    Figure,
    Math,
    Matrix,
    Plot,
    Section,
    Subsection,
    Tabular,
    TikZ,
)
from pylatex.utils import italic

def save_to_file_csv(strategy_results, filename):
    list_to_export = []
    for strategy in strategy_results:
        if not "Name" in strategy.statistics.keys():
            strategy.statistics["Name"] = chart.string_from_dict(strategy.name)
        pass
        list_to_export.append(strategy.statistics)
    pass
    df= pd.DataFrame(list_to_export)
    column_to_move = df.pop("Name")
    df.insert(0, "Name", column_to_move)
    df.to_csv(filename)

def save_to_file_latex(strategy_results, stats_and_plots,prices, filename):
    if filename != '':
        if shutil.which('latex'):
            dirname = os.path.dirname(__file__)
            tempdir = os.path.join(dirname,'chartsTemp/')
            geometry_options = {"tmargin": "1cm", "lmargin": "1cm"}
            doc = Document(geometry_options=geometry_options)


            for strategy in strategy_results:
                chart.create_chart(prices, strategy, 'chartsTemp/')
                with doc.create(Section(chart.string_from_dict(strategy.name))):
                    for statistic in strategy.statistics:
                        doc.append(statistic + ': '  + str(strategy.statistics[statistic]))
                        doc.append("\n")
                    with doc.create(Figure(position="h!")) as plot:
                        plot.add_image(tempdir + chart.string_from_dict(strategy.name) +'.png')
            doc.generate_pdf(filename, clean_tex=True)
            chart.clean_dir(tempdir)
        else:
            print("Unable to find latex, which is necessary to generate pdf.")

    pass