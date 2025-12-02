import 'package:http/http.dart' as http;
import 'api_config.dart' as api_config;
import 'dart:convert';



class ApiService {
  api_config.Api  api = api_config.Api();

  static Future<List<String>?> fetchAvailableStrategies() async {
    final response = await http.get(Uri.parse(api_config.Api.avalibleDefaultStartegies));

    if (response.statusCode == 200) {
      // Assuming the response body is a JSON array of strings
      List<String> strategies = List<String>.from(json.decode(response.body));
      return strategies;
    } else {
      throw Exception('Failed to load avalible strategies');
    }
  }

  static Future<List<String>?> fetchMetrics() async {
    final response = await http.get(Uri.parse(api_config.Api.metrics));

    if (response.statusCode == 200) {
      // Assuming the response body is a JSON array of strings
      List<String> metrics = List<String>.from(json.decode(response.body));
      return metrics;
    } else {
      throw Exception('Failed to load metrics');
    }
  }

  static Future<Map<String,dynamic>?> validateStrategy(String strategyName, String strategyCode) async {
    try{
      final response = await http.post(
        Uri.parse(api_config.Api.validateStrategy),
        headers: {'Content-Type': 'application/json'},
        body: json.encode({'strategy_name' : strategyName,'strategy_code': strategyCode}),
      );

      if (response.statusCode == 200) {
        // Assuming the response body contains a JSON object with a 'valid' field
        var result = json.decode(response.body);
        return result;
      } else {
        return {'valid' : false, 'message' : 'Server error: ${response.statusCode}'};
      }
    }
   catch(e){
      return {
        'valid': false,
        'message': 'Connection error: $e',
      };
    }
  }


  static Future<Map<String,dynamic>?> fetchStrategyParameters(String strategyName) async {
    final response = await http.get(Uri.parse(api_config.Api.strategyDict + strategyName));

    if (response.statusCode == 200) {
      // Assuming the response body contains a JSON object with parameters
      var result = json.decode(response.body);
      return result;
    } else {
      throw Exception('Failed to load strategy parameters');
    }
  }

  static Future<bool> runStrategy(String strategyName, String strategyCode, List<Map<String, dynamic>> prices,
  Map<String,dynamic> parameters,
    double startingBalance, double minComission, double comissionFactor, List<String> metrics,) async {
    try{
      final response = await http.post(
        Uri.parse(api_config.Api.runStartegy),
        headers: {'Content-Type': 'application/json'},
        body: json.encode({
          'strategy_name': strategyName,
          'strategy_code': strategyCode,
          'prices': prices,
          'parameters': parameters,
          'starting_balance': startingBalance,
          'min_comission': minComission,
          'comission_factor': comissionFactor,
          'metrics': metrics,
        }),
      );

      if (response.statusCode == 200) {
        // Assuming the response body contains a JSON object with a 'success' field
        var result = json.decode(response.body);
        return result['success'];
      } else {
        throw Exception('Failed to run strategy');
      }
    }
    catch(e){
      throw Exception('Connection error: $e');
    }
  }
}

