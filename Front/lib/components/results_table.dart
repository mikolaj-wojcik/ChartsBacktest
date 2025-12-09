import 'package:flutter/material.dart';
import '../api/excel.dart';
import '../api/backtest_result.dart';
import 'package:data_table_2/data_table_2.dart';

class ResultsTable extends StatelessWidget {
  final List<BacktestResult> results;
  final String excelFileName;

  ResultsTable({super.key, required this.results, this.excelFileName = 'backtest_results.xlsx'});

  List<DataColumn> _buildColumns(List<BacktestResult> backtestResults) {
    List<DataColumn> columns = [
      DataColumn2(label: Text('Name'),minWidth: 150),
      DataColumn2(label: Text('Balance')),
    ];

    if (backtestResults.isNotEmpty) {
      backtestResults.first.statistics.keys.forEach((key) {
        columns.add(DataColumn2(
          label: ConstrainedBox(
            constraints: const BoxConstraints(maxWidth: 120),
            child: Text(
              key,
              softWrap: true,
              maxLines: 2,
              overflow: TextOverflow.ellipsis,
              textAlign: TextAlign.center,
            ),
          ),
          size: ColumnSize.M,
        ));
      });
    }

    columns.add(DataColumn2(label: Text(''))); // For charts
    columns.add(DataColumn2(label: Text(''))); // For downloading Excel

    return columns;
  }

  List<DataRow> _buildRows(List<BacktestResult> backtestResults) {
    return backtestResults.map((result) {
      List<DataCell> cells = [
        DataCell(Text(result.strategyName.name)),
        DataCell(Text(result.balance.toStringAsFixed(2))),
      ];

      result.statistics.forEach((key, value) {
        cells.add(DataCell(Text(value.toStringAsFixed(2))));
      });

      cells.add(DataCell(IconButton(
        icon: Icon(Icons.show_chart),
        onPressed: () {
          // Implement chart display logic here
        },
      )));

      cells.add(DataCell(
        IconButton(
        icon: Icon(Icons.download),
        onPressed: () async {
          await ExcelExporter.exportTransactionsToExcel(result.transactions, fileName: '${result.strategyName.name}_transactions.xlsx');
        },
      )));

      return DataRow(cells: cells);
    }).toList();
  }
  @override
  Widget build(BuildContext context) {
    final backtestResults = results;

    if (backtestResults.isEmpty) {
      return const Center(child: Text('No results available'));
    }

    return LayoutBuilder(
      builder: (context, constraints) {
        final minWidth = backtestResults.first.statistics.length * 100.0 + 200;
        
        return 
            ConstrainedBox(
              constraints: BoxConstraints(
                minWidth: constraints.maxWidth,
                minHeight: constraints.maxHeight,
              ),
              child: DataTable2(
                columnSpacing: 12,
                horizontalMargin: 12,
                minWidth: minWidth > constraints.maxWidth ? minWidth : constraints.maxWidth,
                columns: _buildColumns(backtestResults),
                rows: _buildRows(backtestResults),
              ),
            
            );
          
        
      },
    );
  }
}