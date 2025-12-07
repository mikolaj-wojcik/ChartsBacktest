import 'dart:io';

import 'package:flutter/material.dart';
import 'components/strategies_dropdown.dart';
import 'api/api_service.dart';
import 'components/files_load.dart';
import 'components/dynamic_params_table.dart';
import 'components/prices_loader.dart';
import 'components/metrics_checkbox.dart';
import 'components/comission_fields.dart';

class App extends StatelessWidget {
  const App({super.key});

  @override
  Widget build(BuildContext context) {
    return const MaterialApp(
      debugShowCheckedModeBanner: false,
      home: ParamScreen(),
    );
  }
}

class ParamScreen extends StatefulWidget {
  const ParamScreen({super.key});

  @override
  State<ParamScreen> createState() => _ParamScreenState();
}

class _ParamScreenState extends State<ParamScreen> {
  String title = 'Backtest Configuration';
  List<String>? strategies;
  bool isLoading = false;
  bool isLoadingParams = false;
  String? errorMessage;
  String? selectedStrategy;
  double? startingBalance;
  double? minComission;
  double? comissionFactor;
  List<Map<String, dynamic>>? pricesJson;
  Map<String, dynamic>? parameters;
  Map<String, bool> metrics = {};
  String? strategyCode;
  String? startegyName;
  final GlobalKey<DynamicParamsTableState> paramsTableKey =
      GlobalKey<DynamicParamsTableState>();

  final GlobalKey<FileLoaderState> fileLoaderKey =
      GlobalKey<FileLoaderState>();
  
  static const Map<String, String> _dummyParams = {
    ' ': 'int',
  };

  Future<void> _loadStrategies() async {
    setState(() {
      isLoading = true;
      errorMessage = null;
    });

    try {
      final fetchedStrategies = await ApiService.fetchAvailableStrategies();
      setState(() {
        strategies = fetchedStrategies;
        strategies!.add("Own strategy");
      });
    } catch (e) {
      setState(() {
        errorMessage = 'Error loading strategies: $e';
      });
    } finally {
      setState(() {
        isLoading = false;
      });
    }
  }

  Future<void> _loadParams() async {
    setState(() {
      isLoadingParams = true;
      errorMessage = null;
    });

    try {
      if (selectedStrategy != 'Own strategy') {
        final fetchedParams =
            await ApiService.fetchStrategyParameters(selectedStrategy!);
        setState(() {
          parameters = fetchedParams;
        });
      } else {
        setState(() {
          parameters = null;
        });
      }
    } catch (e) {
      setState(() {
        errorMessage = 'Error loading parameters: $e';
      });
    } finally {
      setState(() {
        isLoadingParams = false;
      });
    }
  }

  Future<void> _loadMetrics() async {
    setState(() {
      isLoading = true;
      errorMessage = null;
    });

    try {
      final fetchedMetrics = await ApiService.fetchMetrics();
      Map<String, bool> initialSelected = {};
      for (var metric in fetchedMetrics!) {
        initialSelected[metric] = false;
      }
      setState(() {
        metrics = initialSelected;
      });
    } catch (e) {
      setState(() {
        errorMessage = 'Error loading metrics: $e';
      });
    } finally {
      setState(() {
        isLoading = false;
      });
    }
  }

  Future<void> _runStrategy() async {
     if (startingBalance == null || startingBalance! <= 0){
      _showError('Please fill starting balance before running the strategy.');
      return;
    }
    if (minComission == null || comissionFactor == null){
      _showError('Please fill all commission fields before running the strategy.');
      return;
    }
    if (pricesJson == null || pricesJson!.isEmpty){
      _showError('Please load price data before running the strategy.');
      return;
    }
    if (selectedStrategy == "Own strategy" && (strategyCode == null || strategyCode!.isEmpty)){
      _showError('Please provide valid strategy code for "Own strategy".');
      return;
    }
    Map<String, String> ?  params = paramsTableKey.currentState?.getValues();
    if(params == null || params.isEmpty){return;}

    await ApiService.runStrategy(
      selectedStrategy == "Own strategy" ? startegyName! : selectedStrategy!,
      selectedStrategy == "Own strategy" ? strategyCode! : '',
      pricesJson!,
      params,
      startingBalance!,
      minComission!,
      comissionFactor!,
      metrics.entries.where((entry) => entry.value).map((entry) => entry.key).toList(),
    );


  }
  @override
  void initState() {
    super.initState();
    _loadStrategies();
    _loadMetrics();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(title),
      ),
      body: isLoading
          ? const Center(child: CircularProgressIndicator())
          : errorMessage != null
              ? Center(child: Text(errorMessage!))
              : strategies != null
                  ? SingleChildScrollView( 
                      padding: const EdgeInsets.all(16),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.center,
                        children: [
                          // Strategy Dropdown
                          StatefulBuilder(builder: ( context, setDropdownState) {
                          return StrategiesDropdown(
                            startegies: strategies!,
                            onSelected: (String strategy) {
                              if (strategy == selectedStrategy) return;
                              setState(() {
                                title = 'Selected: $strategy';
                                selectedStrategy = strategy;
                                selectedStrategy != 'Own strategy' ? strategyCode = null : null;
                              });
                              _loadParams();
                              selectedStrategy != 'Own strategy' ? fileLoaderKey.currentState?.reset(): null;

                            },
                          );
                        }),
                          const SizedBox(height: 20),
                          ComissionFields(onBalanceChanged: (value){
                            startingBalance = value;},
                           onMinComissionChanged: (value){
                            minComission = value;},
                            onComssionFactorChanged: (value){
                            comissionFactor = value;},),
                          const SizedBox(height: 10),
                          // Prices Loader
                          PricesLoader(
                            enabled: true,
                            onPricesLoaded: (prices) {
                              setState(() {
                                pricesJson = prices;
                              });
                            },
                          ),
                          const SizedBox(height: 10),

                          // Strategy File Loader

                          FileLoader(
                            key: fileLoaderKey,
                            onFileSelected: (fil) {
                              print('Selected file: ${fil.path}');
                            },
                            enabled: selectedStrategy == "Own strategy",
                            onParametersChanged: (paramMap) {
                              setState(() {
                                parameters = paramMap.isEmpty ? null : paramMap;
                              });
                            },
                            onCodeValidation: (name, code) {
                              setState(() {
                                startegyName = name;
                                strategyCode = code;
                              });
                            },
                          ),
                          const SizedBox(height: 20),

                          // Loading indicator for params
                          if (isLoadingParams)
                            const Padding(
                              padding: EdgeInsets.all(20.0),
                              child: CircularProgressIndicator(),
                            )
                          else
                            // Parameters Table
                             SizedBox(
                                    width: 350,
                                    child: DynamicParamsTable(
                                      key: paramsTableKey,
                                      rows: parameters != null
                                          ?
                                      Map<String, String>.fromEntries(
                                        parameters!.entries.map((entry) {
                                          String type = 'string';
                                          if (entry.value is int) {
                                            type = 'int';
                                          } else if (entry.value is double) {
                                            type = 'float';
                                          }
                                          return MapEntry(entry.key, type);
                                        }),
                                      ) : _dummyParams,
                                      enabled: parameters != null,
                                    ),
                                  ),
                          const SizedBox(height: 20),

                          // Metrics Checkbox
                        if (metrics.isNotEmpty)
                          const Text('Select Metrics to Calculate'),
                          const SizedBox(height: 8),
                          Container(
                            width: 350,
                            height: 300, // Fixed height
                            decoration: BoxDecoration(
                              border: Border.all(color: Colors.grey),
                              borderRadius: BorderRadius.circular(4),
                            ),
                            child: Scrollbar(
                              thumbVisibility: true, // Always show scrollbar
                             child: SingleChildScrollView(
                                padding: const EdgeInsets.all(8),
                                child: StatefulBuilder(
                                  builder: (BuildContext context, StateSetter setMetricsState) {
                                    return MetricsCheckbox(
                                      metrics: metrics,
                                      onChanged: (String metric, bool value) {
                                        setMetricsState(() {
                                          metrics[metric] = value;
                                        });
                                      },
                                    );
                                    },
                                  ),
                                ),
                              ),
                            ),
                        ],
                      ),
                    )
                  : const Center(child: Text('No strategies available.')),
      floatingActionButton: FloatingActionButton(
        onPressed: () {_runStrategy();},
        child: const Icon(Icons.play_arrow),
      ),
    );
  }
void _showError(String message) {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Error'),
        content: Text(message),
        actions: [
          TextButton(
            onPressed: () => Navigator.of(context).pop(),
            child: const Text('OK'),
          ),
        ],
      ),
    );
  }
}