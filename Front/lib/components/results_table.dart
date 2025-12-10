import 'package:flutter/material.dart';
import '../api/excel.dart';
import '../api/backtest_result.dart';
import 'package:data_table_2/data_table_2.dart';

class ResultsTable extends StatefulWidget {
  final List<BacktestResult> results;
  final String excelFileName;

  ResultsTable({super.key, required this.results, this.excelFileName = 'backtest_results.xlsx'});

  @override
  State<ResultsTable> createState() => _ResultsTableState();
}

class _ResultsTableState extends State<ResultsTable> {
  int? _sortedColumnIndex;
  bool _isAscending = true;

  late List<BacktestResult> sortedResults;

  @override
  void initState() {
    super.initState();
    sortedResults = List.from(widget.results);
  }

  void _sort<T>(Comparable<T> Function(BacktestResult d) getField, int columnIndex, bool ascending) {
    sortedResults.sort((a, b) {
      final aValue = getField(a);
      final bValue = getField(b);
      return ascending ? Comparable.compare(aValue, bValue) : Comparable.compare(bValue, aValue);
    });
    setState(() {
      _sortedColumnIndex = columnIndex;
      _isAscending = ascending;
    });
  }


  List<DataColumn> _buildColumns(List<BacktestResult> backtestResults) {
    List<DataColumn> columns = [
      DataColumn2(headingRowAlignment: MainAxisAlignment.center, label: Text('Name'),minWidth: 150, ),
      DataColumn2(headingRowAlignment: MainAxisAlignment.center, label: Text('Balance'), numeric: true,
          onSort: (columnIndex, ascending) {
        _sort<num>((d) => d.balance, columnIndex, ascending);
      }),
    ];

    if (sortedResults.isNotEmpty) {
      int colIndex = 2;
      for (var key in sortedResults.first.statistics.keys) {
        final currentKey = key;
        final currentIndex = colIndex;

      
        columns.add(DataColumn2(
          headingRowAlignment: MainAxisAlignment.center,
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
          numeric: true,
          onSort: (columnIndex, ascending) {
            _sort<num>((d) => d.statistics[currentKey] ?? 0, currentIndex, ascending);
          },
        ));
        colIndex++;
      }
    }

    columns.add(DataColumn2(headingRowAlignment: MainAxisAlignment.center, label: Text(''))); // For charts
    columns.add(DataColumn2(headingRowAlignment: MainAxisAlignment.center, label: Text(''))); // For downloading Excel

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
    final backtestResults = sortedResults;

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
                sortColumnIndex: _sortedColumnIndex,
                sortAscending: _isAscending,
              ),
            
            );
          
        
      },
    );
  }
}