
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
          toolbarHeight: 70,
          title: Column(
            children: [
              Text(widget.strategyName),
              
              Container(
                alignment: Alignment.center,
                padding: const EdgeInsets.all(5),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    Row(
                      children: [
                        Container(
                          width: 12,
                          height: 12,
                          decoration: BoxDecoration(
                            color: const Color.fromARGB(255, 225, 255, 0),
                            border: Border.all(color: Colors.black, width: 1),
                          ),
                        ),
                        const SizedBox(width: 6),
                        const Text('Buy', style: TextStyle(fontSize: 12)),
                      ],
                    ),
                    const SizedBox(width: 20),
                    Row(
                      children: [
                        Container(
                          width: 12,
                          height: 12,
                          decoration: BoxDecoration(
                            color: const Color.fromARGB(255, 0, 255, 0),
                            shape: BoxShape.circle,
                            border: Border.all(color: Colors.black, width: 1),
                          ),
                        ),
                        const SizedBox(width: 6),
                        const Text('Sell (Profit)', style: TextStyle(fontSize: 12)),
                      ],
                    ),
                    const SizedBox(width: 20),
                    Row(
                      children: [
                        Container(
                          width: 12,
                          height: 12,
                          decoration: BoxDecoration(
                            color: const Color.fromARGB(255, 255, 0, 0),
                            shape: BoxShape.circle,
                            border: Border.all(color: Colors.black, width: 1),
                          ),
                        ),
                        const SizedBox(width: 6),
                        const Text('Sell (Loss)', style: TextStyle(fontSize: 12)),
                      ],
                    ),
                  ],
                ),
              ),
            
            ]
          )
        ),
        body: Padding(
          padding: const EdgeInsets.all(10.0),
          child: TransactionsChart(transactions: widget.transactions, pricesJson: widget.pricesJson, transactionCandles: widget.transactions.map((tr) => tr.candle).toList()),
        ),
      );
  }
}