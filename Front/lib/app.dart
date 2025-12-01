import 'package:flutter/material.dart';
import 'components/strategies_dropdown.dart';
import 'api/api_service.dart';
import 'components/files_load.dart';
import 'components/dynamic_params_table.dart';
import 'components/prices_loader.dart';
import 'components/metrics_checkbox.dart';

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
  List<Map<String, dynamic>>? pricesJson;
  Map<String, dynamic>? parameters;
  Map<String, bool> metrics = {};
  String? strategyCode;
  final GlobalKey<DynamicParamsTableState> paramsTableKey =
      GlobalKey<DynamicParamsTableState>();
  
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
                  ? SingleChildScrollView( // ← KEY FIX: Add scrolling
                      padding: const EdgeInsets.all(16),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.center,
                        children: [
                          // Strategy Dropdown
                          StrategiesDropdown(
                            startegies: strategies!,
                            onSelected: (String strategy) {
                              setState(() {
                                title = 'Selected: $strategy';
                                selectedStrategy = strategy;
                              });
                              _loadParams();
                            },
                          ),
                          const SizedBox(height: 20),

                          // Prices Loader
                          PricesLoader(
                            enabled: true,
                            onPricesLoaded: (prices) {
                              setState(() {
                                pricesJson = prices;
                              });
                            },
                          ),
                          const SizedBox(height: 20),

                          // Strategy File Loader
                          const Text('Strategy file'),
                          const SizedBox(height: 8),
                          FileLoader(
                            onFileSelected: (fil) {
                              print('Selected file: ${fil.path}');
                            },
                            enabled: selectedStrategy == "Own strategy",
                            onParametersChanged: (paramMap) {
                              setState(() {
                                parameters = paramMap.isEmpty ? null : paramMap;
                              });
                            },
                            onCodeValidation: (code) {
                              setState(() {
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
                            parameters != null
                                ? SizedBox(
                                    width: 350,
                                    child: DynamicParamsTable(
                                      key: paramsTableKey,
                                      rows: Map<String, String>.fromEntries(
                                        parameters!.entries.map((entry) {
                                          String type = 'string';
                                          if (entry.value is int) {
                                            type = 'int';
                                          } else if (entry.value is double) {
                                            type = 'float';
                                          }
                                          return MapEntry(entry.key, type);
                                        }),
                                      ),
                                    ),
                                  )
                                : const SizedBox(
                                    width: 350,
                                    child: DynamicParamsTable(
                                      rows: _dummyParams,
                                      enabled: false,
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
                                child: MetricsCheckbox(
                                  metrics: metrics,
                                  onChanged: (String metric, bool value) {
                                    setState(() {
                                      metrics[metric] = value;
                                    });
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
        onPressed: () {
          if (paramsTableKey.currentState != null) {
            final values = paramsTableKey.currentState!.getValues();
            print('Parameter values: $values');
            
            // Get selected metrics
            List<String> selectedMetrics = metrics.entries
                .where((entry) => entry.value)
                .map((entry) => entry.key)
                .toList();
            
            print('Selected metrics: $selectedMetrics');
            print('Prices: ${pricesJson?.length ?? 0} records');
            print('Strategy: $selectedStrategy');
          } else {
            print('Params table state is null');
          }
        },
        child: const Icon(Icons.play_arrow),
      ),
    );
  }
}