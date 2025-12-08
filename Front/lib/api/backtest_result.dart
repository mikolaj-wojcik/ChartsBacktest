import 'dart:convert';

class BacktestResult {
  late StrategyName strategyName;
  late Map<String, double> statistics;
  late double balance;
  late List<Transaction> transactions;

  BacktestResult(resultsRow) {
    strategyName = StrategyName(resultsRow['name']);

    // Convert statistics (possibly a _JsonMap) to Map<String,double>
    final rawStats = resultsRow['statistics'];
    if (rawStats is Map) {
      final tmp = Map<String, dynamic>.from(rawStats);
      statistics = tmp.map((k, v) => MapEntry(k.toString(), (v is num) ? v.toDouble() : double.tryParse(v.toString()) ?? 0.0));
    } else {
      // Fallback: empty map
      statistics = {};
    }

    balance = (resultsRow['balance'] as num).toDouble();
    transactions = (resultsRow['transaction_history'] as List).map((txRow) => Transaction(txRow)).toList();
  }

}

class StrategyName {
  String name = '';
  Map<String, num> parameters = {};

  StrategyName(Map<String, dynamic> nameDict) {
    name = jsonEncode(nameDict).replaceAll('{', '').replaceAll('}', '').replaceAll('"', '');
    parameters = nameDict.map((key, value) => MapEntry(key, (value as num)));
  }
}

class Transaction {
  late int candle;
  late double size;
  late double price;
  late double commission;
  late double profit;
  late double balance;

  Transaction(transactionRow) {
    candle = (transactionRow['candle'] as num).toInt();
    size = (transactionRow['size'] as num).toDouble();
    price = (transactionRow['price'] as num).toDouble();
    commission = (transactionRow['commission'] as num).toDouble();
    profit = (transactionRow['profit'] as num).toDouble();
    balance = (transactionRow['balance'] as num).toDouble();
  }
}
