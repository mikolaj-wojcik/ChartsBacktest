import 'package:excel/excel.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import '../api/excel.dart';
import '../api/backtest_result.dart';
import '../app.dart';

class ResultsTable extends StatelessWidget {
  final List<BacktestResult> results;
  final String excelFileName;

  ResultsTable({super.key, required this.results, this.excelFileName = 'backtest_results.xlsx'});

  List<DataColumn> _buildColumns(List<BacktestResult> backtestResults) {
    List<DataColumn> columns = [
      DataColumn(label: Text('Name')),
      DataColumn(label: Text('Balance')),
    ];

    if (backtestResults.isNotEmpty) {
      backtestResults.first.statistics.keys.forEach((key) {
        columns.add(DataColumn(label: Text(key)));
      });
    }

    columns.add(DataColumn(label: Text(''))); // For charts
    columns.add(DataColumn(label: Text(''))); // For downloading Excel

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

      cells.add(DataCell(IconButton(
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
    List<BacktestResult> backtestResults = results;

    return Column(
      children: [
        Expanded(
          child: SingleChildScrollView(
            scrollDirection: Axis.horizontal,
            child: DataTable(
              columns: _buildColumns(backtestResults),
              rows: _buildRows(backtestResults),
            ),
          ),
        ),
      ],
    );
  }
}