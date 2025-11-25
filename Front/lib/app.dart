

import 'package:flutter/material.dart';
import 'components/strategies_dropdown.dart';
import 'api/api_service.dart';

class App extends StatelessWidget {
  const App({super.key});

  @override
  Widget build(BuildContext context) {
    return const MaterialApp(
      debugShowCheckedModeBanner: false,
      home: ParamScreen()
    );
  }
}


class ParamScreen extends StatefulWidget {
  const ParamScreen({super.key});

  @override
  State<ParamScreen> createState() => _ParamScreenState();
}


class _ParamScreenState extends State<ParamScreen> {
  String title = 'ABC';
  List<String>? strategies;
  List<String>? metrics;
  bool isLoading = false;
  String? errorMessage;
  String? selectedStrategy;
  
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

  Future<void> _loadMetrics() async {
    setState(() {
      isLoading = true;
      errorMessage = null;
    });

    try {
      final fetchedMetrics = await ApiService.fetchMetrics();
      setState((){
        metrics = fetchedMetrics;
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
      body: Center( 
        child: isLoading
          ? const CircularProgressIndicator()
          : errorMessage != null
              ? Text(errorMessage!)
              : strategies != null
                  ? Column(children: [
                      StrategiesDropdown(
                        startegies: strategies!,
                        onSelected: (String strategy) {
                          setState(() {
                            title = 'Selected: $strategy';
                            selectedStrategy = strategy;
                          });
                        },
                      ),
                      Text('Startegy file'),
                      TextField(
                        enabled: selectedStrategy == "Own strategy",
                        decoration: const InputDecoration(
                          border: OutlineInputBorder(),
                          labelText: "Startegy file",
                        ),
                      )
                      
                    ],)
                    : const Text('No strategies available.')
          ),
        
        /*TextField(
        decoration: const InputDecoration(labelText: "Name"),
        onChanged: (value) => title = value,),
        ElevatedButton(
          onPressed: () {
          },
          child: const Text('Update Title'),
        ),
      ],),*/
      floatingActionButton: FloatingActionButton(
        onPressed: _loadStrategies,
        child: const Icon(Icons.refresh)
      ),
    );
  }
}