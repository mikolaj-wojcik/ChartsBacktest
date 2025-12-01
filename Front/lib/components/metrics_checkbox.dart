import 'package:flutter/material.dart';

class MetricsCheckbox extends StatelessWidget {
  final Map<String, bool> metrics;
  final Function(String, bool) onChanged;

  const MetricsCheckbox({super.key, required this.metrics, required this.onChanged});

  @override
  Widget build(BuildContext context) {
    return Column(
      children: metrics.keys.map((String metric) {
        return CheckboxListTile(
          title: Text(metric),
          value: metrics[metric],
          onChanged: (bool? value) {
            if (value != null) {
              onChanged(metric, value);
            }
          },
        );
      }).toList(),
    );
  }
  
}