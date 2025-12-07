import 'dart:convert';

class BacktestResult {
  late StrategyName strategyName;
  late List<Map<String, double>> statistics;
  late double balance;
  late List<Transaction> transactions;

  BacktestResult(resultsRow) {
    strategyName = StrategyName(resultsRow['name']);

    // Convert statistics entries to Map<String, double>
    statistics = resultsRow['statistics'];

    balance = (resultsRow['balance'] as num).toDouble();
    transactions = (resultsRow['transactions'] as List).map((txRow) => Transaction(txRow)).toList();
  }

}

class StrategyName {
  String name = '';
  Map<String, num> parameters = {};

  StrategyName(Map<String, dynamic> nameDict) {
    name = jsonEncode(nameDict).replaceAll('{', '').replaceAll('}', '').replaceAll('"', '');
    parameters = nameDict.map((k, v) => MapEntry(k.toString(), (v is num) ? v : (num.tryParse(v.toString()) ?? 0)));
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
