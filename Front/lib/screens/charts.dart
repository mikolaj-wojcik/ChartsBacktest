
import 'package:flutter/material.dart';
import 'package:fl_chart/fl_chart.dart';
import '../api/backtest_result.dart';
import '../components/transactions_chart.dart';

class Charts extends StatefulWidget {
  final String strategyName;
  final List<Map<String, dynamic>> pricesJson;
  final List<Transaction> transactions;

  const Charts({super.key, required this.strategyName, required this.transactions,required this.pricesJson});
  @override
  State<Charts> createState() => _ChartsState();
}


class _ChartsState extends State<Charts>{

  @override
  Widget build(BuildContext context){
      return Scaffold(
        appBar: AppBar(
          title: Text(widget.strategyName),
        ),
        body: Padding(
          padding: const EdgeInsets.all(16.0),
          child: TransactionsChart(transactions: widget.transactions, pricesJson: widget.pricesJson)
      )
      );
  }
}