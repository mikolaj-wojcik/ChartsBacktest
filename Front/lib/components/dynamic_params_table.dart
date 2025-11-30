

import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

class DynamicParamsTable extends StatefulWidget {
  final Map<String, String> rows; // {'value1': 'int', 'value2': 'float'}
  final bool enabled;
  
  const DynamicParamsTable({
    super.key,
    required this.rows,
    this.enabled = true,
  });

  @override
  State<DynamicParamsTable> createState() => _DynamicParamsTable();
}

class _DynamicParamsTable extends State<DynamicParamsTable> {
  late Map<String, Map<String, TextEditingController>> controllers;

  @override
  void initState() {
    super.initState();
    _initializeControllers();
  }

  @override
  void didUpdateWidget(DynamicParamsTable oldWidget) {
    super.didUpdateWidget(oldWidget);
    
    // Check if rows changed
    if (oldWidget.rows != widget.rows) {
      // Dispose old controllers
      controllers.forEach((key, row) {
        row.forEach((col, controller) {
          controller.dispose();
        });
      });
      
      // Reinitialize with new rows
      _initializeControllers();
    }
  }
  void _initializeControllers() {
    controllers = {};
    widget.rows.forEach((key, type) {
      controllers[key] = {
        'min': TextEditingController(),
        'max': TextEditingController(),
        'step': TextEditingController(),
      };
    });
  }

  @override
  void dispose() {
    controllers.forEach((key, row) {
      row.forEach((col, controller) {
        controller.dispose();
      });
    });
    super.dispose();
  }

  // Get values based on type (int or float)
  Map<String, Map<String, num?>> getValues() {
    Map<String, Map<String, num?>> values = {};
    
    controllers.forEach((rowKey, row) {
      String type = widget.rows[rowKey]!;
      
      if (type == 'int') {
        values[rowKey] = {
          'min': int.tryParse(row['min']!.text),
          'max': int.tryParse(row['max']!.text),
          'step': int.tryParse(row['step']!.text),
        };
      } else {
        values[rowKey] = {
          'min': double.tryParse(row['min']!.text),
          'max': double.tryParse(row['max']!.text),
          'step': double.tryParse(row['step']!.text),
        };
      }
    });
    
    return values;
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      height: 200, // Height for ~4 rows + header
      decoration: BoxDecoration(
        border: Border.all(color: Colors.grey),
        borderRadius: BorderRadius.circular(4),
      ),
      child: Scrollbar(
        thumbVisibility: true,
        child: SingleChildScrollView(
          scrollDirection: Axis.vertical,
          child: DataTable(
            headingRowHeight: 40,
            dataRowMinHeight: 50,
            dataRowMaxHeight: 50,
            columnSpacing: 20,
            columns: const [
              DataColumn(label: Text('Parameter', style: TextStyle(fontWeight: FontWeight.bold))),
              DataColumn(label: Text('Min', style: TextStyle(fontWeight: FontWeight.bold))),
              DataColumn(label: Text('Max', style: TextStyle(fontWeight: FontWeight.bold))),
              DataColumn(label: Text('Step', style: TextStyle(fontWeight: FontWeight.bold))),
            ],
            rows: controllers.entries.map((entry) {
              String rowName = entry.key;
              Map<String, TextEditingController> rowControllers = entry.value;
              String type = widget.rows[rowName]!;

              return DataRow(
                cells: [
                  DataCell(Text(rowName)),
                  DataCell(_buildCell(rowControllers['min']!, type, )),
                  DataCell(_buildCell(rowControllers['max']!, type)),
                  DataCell(_buildCell(rowControllers['step']!, type)),
                ],
              );
            }).toList(),
          ),
        ),
      ),
    );
  }

  Widget _buildCell(TextEditingController controller, String type) {
    return Container(
    child :Padding(
      padding: const EdgeInsets.all(4.0),
      child: TextField(
        enabled: widget.enabled,
        controller: controller,
        keyboardType: type == 'int'
            ? TextInputType.number
            : const TextInputType.numberWithOptions(decimal: true),
        inputFormatters: type == 'int'
            ? [FilteringTextInputFormatter.digitsOnly]
            : [FilteringTextInputFormatter.allow(RegExp(r'^\d*\.?\d*'))],
        textAlign: TextAlign.center,
        decoration: const InputDecoration(
          border: InputBorder.none,
          isDense: true,
          contentPadding: EdgeInsets.symmetric(vertical: 8, horizontal: 4),
        ),
      ),
    ),
    );
  }
}