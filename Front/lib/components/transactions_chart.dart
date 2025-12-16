import 'package:flutter/material.dart';
import 'package:fl_chart/fl_chart.dart';
import '../api/backtest_result.dart';

class TransactionsChart extends StatelessWidget {
  final List<Transaction> transactions;
  final List<Map<String, dynamic>> pricesJson;
  final List<int>? transactionCandles;
  

  const TransactionsChart({super.key, required this.transactions, required this.pricesJson, required this.transactionCandles});
  
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
                      if (transactionCandles == null) {return FlDotCirclePainter(radius: 2, color: Colors.transparent);}
                      if (transactionCandles!.contains(spot.x.ceil())) {
                      final tx = transactions.firstWhere((t) => t.candle == spot.x.ceil(), orElse: () => Transaction.empty());
                        // Arrow up for buy/profit, down for sell/loss
                        return tx.size > 0 ? FlDotSquarePainter(size: 8, color: const Color.fromARGB(255, 225, 255, 0), strokeColor: const Color.fromARGB(255, 0, 0, 0)) : FlDotCirclePainter(radius: 4, strokeWidth: 1.0, color: tx.profit > 0.0 ? const Color.fromARGB(255, 0, 255, 0): const Color.fromARGB(255, 255, 0, 0), strokeColor: const Color.fromARGB(255, 0, 0, 0));
                      }
                      return FlDotCirclePainter(radius: 2, color: Colors.transparent);
                    },
                    ),
                  ),
                ],

                lineTouchData: transactionCandles != null ? LineTouchData(
                  enabled: true,
                  touchTooltipData: LineTouchTooltipData(
                    getTooltipItems: (List<LineBarSpot> spots){
                      return spots.map((spot) {
                        if (transactionCandles!.contains(spot.x.ceil())) {
                          final tx = transactions.firstWhere((t) => t.candle == spot.x.ceil(), orElse: () => Transaction.empty());
                          if (tx.candle != 0) {
                            return LineTooltipItem(
                            tx.size > 0.0 ? 'Buy\n' : 'Sell\n',
                            const TextStyle(
                                color: Colors.white,
                                fontWeight: FontWeight.bold,
                              ),
                            children: [
                              TextSpan(text: 'Size: ${tx.size.abs()}\n'),
                              TextSpan(text: 'Price: ${tx.price}\n'),
                              TextSpan(text: 'Comission: ${tx.commission}\n'),
                              tx.profit != 0.0 ? TextSpan(text: 'Profit: ${tx.profit}\n') :TextSpan()
                            ]

                            
                          );
                          }
                        }
                    }).toList();


                    }
                  )




                ) : LineTouchData(enabled: false),
              ),
            ),
            // Overlay symbols
          ],
        );
  }
}