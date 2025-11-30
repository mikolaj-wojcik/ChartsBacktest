import 'package:csv/csv.dart';


class CsvService {
  static bool isValidPricesStruct(List<Map<String, dynamic>> prices) {

    DateTime? prevDate;

    if (prices.isEmpty) return false;
    
    final requiredKeys = {'date', 'open', 'high', 'low', 'close', 'volume'};
    
    for (var price in prices) {
      if (!requiredKeys.every((key) => price.containsKey(key))) {
        return false;
      }

      if (price['date'] == null ||
          price['open'] == null ||
          price['high'] == null ||
          price['low'] == null ||
          price['close'] == null ||
          price['volume'] == null) {
        return false;
      }

      if (prevDate != null){
        DateTime currentDate;
        try {
          currentDate = DateTime.parse(price['date']);
        } catch (e) {
          return false;
        }
        if (!currentDate.isAfter(prevDate)) {
          return false;
        }
        prevDate = currentDate;
      } else {
        try {
          prevDate = DateTime.parse(price['date']);
        } catch (e) {
          return false;
        }
      }

      if (price['open'] is! num ||
          price['high'] is! num ||
          price['low'] is! num ||
          price['close'] is! num ||
          price['volume'] is! num) {
        return false;
      }

      if (price['high'] < price['low'] ||
          price['open'] < 0 ||
          price['high'] < 0 ||
          price['low'] < 0 ||
          price['close'] < 0 ||
          price['volume'] < 0) {
        return false;
      }

      if (price['open'] > price['high'] ||
          price['high'] < price['low'] ||
          price['close'] > price['high']) {
        return false;
      }

      if (price['low'] > price['open'] ||
          price['low'] > price['close']) {
        return false;
      }
    }  
    return true;
  }
  // Parse specific price format (date, open, high, low, close, volume)
  static List<Map<String, dynamic>> parsePricesCsv(String csvString) {
    List<List<dynamic>> csvTable = const CsvToListConverter().convert(csvString);
    
    if (csvTable.isEmpty) {
      return [];
    }

    // Skip header row
    List<Map<String, dynamic>> prices = [];
    
    for (int i = 1; i < csvTable.length; i++) {
      var row = csvTable[i];
      
      prices.add({
        'date': row[0].toString(),
        'open': _parseNumber(row[1]),
        'high': _parseNumber(row[2]),
        'low': _parseNumber(row[3]),
        'close': _parseNumber(row[4]),
        'volume': row.length > 5 ? _parseNumber(row[5]) : 0,
      });
    }
    
    return prices;
  }

  // Helper to parse numbers
  static num _parseNumber(dynamic value) {
    if (value is num) return value;
    if (value is String) {
      return double.tryParse(value) ?? 0;
    }
    return 0;
  }
}