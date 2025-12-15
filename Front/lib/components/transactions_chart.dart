import 'package:flutter/material.dart';
import 'package:fl_chart/fl_chart.dart';
import '../api/backtest_result.dart';

class TransactionsChart extends StatelessWidget {
  final List<Transaction> transactions;
  final List<Map<String, dynamic>> pricesJson;
  

  const TransactionsChart({super.key, required this.transactions, required this.pricesJson});
  
  List<FlSpot> getPricesLine(){
    List<FlSpot> pricesLine = [];
    var candle = 0;
    for (var price in pricesJson){
      candle++;
      pricesLine.add(FlSpot(candle.toDouble(), price['close']));
    }

    return pricesLine;
  }


  @override
  Widget build(BuildContext context) {
    return Stack(
          children: [
            // Chart
            LineChart(
              LineChartData(
                gridData: FlGridData(show: true),
                titlesData: FlTitlesData(
                 bottomTitles: AxisTitles(
                  sideTitles: SideTitles(
                  showTitles: true,
                  reservedSize: 30,
                  getTitlesWidget: (value, meta) {
                    int index = value.toInt();
                    if (index >= 0 && index < pricesJson.length && index%15== 0) {
                      return Text(
                        pricesJson[index]['date'] as String,
                        style: const TextStyle(fontSize: 15),
                      );
                    }
                  return const Text('');
                  },
                ),
                ) ,
                ),
                borderData: FlBorderData(show:true, border: Border(right: BorderSide())),
                lineBarsData: [
                  LineChartBarData(
                    spots: getPricesLine(),
                    isCurved: true,
                    color: Colors.blue,
                    barWidth: 3,
                    dotData: FlDotData(show: true,
                    //checkToShowDot: (spot, barData) {
                    //   return transactions.any((t) => t.candle == spot.x.ceil());
                    //},
                    getDotPainter: (spot, percent, barData, index) {
                      final tx = transactions.firstWhere((t) => t.candle == spot.x.ceil(), orElse: () => Transaction.empty());
    
                      if (tx.candle == 0) {
                      return FlDotCirclePainter(radius: 2, color: Colors.transparent);
                      }
    
                      // Arrow up for buy/profit, down for sell/loss
                      return tx.size > 0 ? FlDotCirclePainter(radius: 4, color: const Color.fromARGB(255, 0, 255, 34)) : FlDotCirclePainter(radius: 4, color: const Color.fromARGB(255, 255, 0, 0));
                    },
                    ),
                  ),
                ],
              ),
            ),
            // Overlay symbols
            Positioned(
              left: 100, // Adjust position
              top: 150,
              child: Container(
                padding: const EdgeInsets.all(4),
                child: const Icon(
                  Icons.arrow_upward,
                  color: Colors.green,
                  size: 25,
                ),
              ),
            ),
            Positioned(
              left: 300,
              top: 50,
              child: Container(
                padding: const EdgeInsets.all(4),
                
                child: const Icon(
                  Icons.arrow_downward,
                  color: Colors.red,
                  size: 25,
                ),
              ),
            ),
          ],
        );
  }
}