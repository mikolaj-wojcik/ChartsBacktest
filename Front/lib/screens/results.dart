import 'package:flutter/material.dart';
import '../api/backtest_result.dart';
import '../api/excel.dart';
import '../components/results_table.dart';


class ResultsScreen extends StatelessWidget {
  final List<BacktestResult> results;
  final List<Map<String, dynamic>>? pricesJson;

  const ResultsScreen({super.key, required this.results, required this.pricesJson});


  void _downloadResults() {
    ExcelExporter.exportToExcel(results);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Backtest Results'),

      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: ResultsTable(results: results),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () {
          _downloadResults();
        },
        child: Icon(Icons.download_rounded),
      ),
    );
  }
}