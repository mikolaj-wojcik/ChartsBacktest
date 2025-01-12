from matplotlib.backends.backend_pdf import PdfPages
import Charts.chartcreator as chart

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

def save_to_file(strategy_results, stats_and_plots,prices, filename):
    tempdir = 'chartsTemp/'
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


    doc.generate_pdf(clean_tex=False)
    chart.clean_dir(tempdir)

    pass