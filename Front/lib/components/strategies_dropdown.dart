

import 'package:flutter/material.dart';

class StrategiesDropdown extends StatefulWidget{

  final List<String> startegies;
  final Function(String) onSelected;

  const StrategiesDropdown({super.key, required this.startegies, required this.onSelected});

  @override
  State<StrategiesDropdown> createState() => _StrategiesDropdownState();
}

class _StrategiesDropdownState extends State<StrategiesDropdown> {
  String? selectedStartegy;

  @override
  Widget build(BuildContext context) {
    return DropdownButton<String>(
      hint: const Text('Select a strategy'),
      value: selectedStartegy,
      items: widget.startegies.map((String strategy) {
        return DropdownMenuItem<String>(
          value: strategy,
          child: Text(strategy),
        );
      }).toList(),
      onChanged: (String? newValue) {
        setState(() {
          selectedStartegy = newValue;
        });
        if (newValue != null) {
          widget.onSelected(newValue);
        }
      },
    );
  }
}



