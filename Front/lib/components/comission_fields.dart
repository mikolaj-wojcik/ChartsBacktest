
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'dart:math' as math;




class ComissionFields extends StatefulWidget {
  final Function(double) onBalanceChanged;
  final Function(double) onMinComissionChanged;
  final Function(double) onComssionFactorChanged;
  


  ComissionFields({super.key, required this.onBalanceChanged, required this.onMinComissionChanged, required this.onComssionFactorChanged, });

  @override
  State<ComissionFields> createState() => _ComissionFieldsState();
}

class _ComissionFieldsState extends State<ComissionFields> {
  double? balance;
  double? minComssion;
  double? comissionFactor;


  bool validComissionFator(double value){
    return value >=0 && value <=1;
  }

  

  
  @override
  Widget build(BuildContext context) {
    return Column(
      children: [Row(children:[
        SizedBox(width: 120,
        child:  Text('Starting balance:'),
        ),
        Container(width: 200, height: 30 ,decoration: 
          BoxDecoration(border: Border.all()), 
          alignment: Alignment.centerLeft,
            child : TextField(  keyboardType: TextInputType.numberWithOptions(decimal: true), // Shows numeric keyboard
              inputFormatters: [
                FilteringTextInputFormatter.allow(RegExp(r'^\d+\.?\d{0,2}'))
              ],textAlignVertical: TextAlignVertical.top,
            onChanged: (value) => {balance = double.tryParse(value) ?? 0.0,
              widget.onBalanceChanged(balance!),},
            decoration: const InputDecoration(
              border: InputBorder.none,
              contentPadding: EdgeInsets.symmetric(horizontal: 2, vertical: -16),
            ),)),
      ]),
      SizedBox(height: 10),
      Row(children:[
        SizedBox(width: 120,
        child:  Text('Minimal comission:'),
        ),
        Container(width: 200, height: 30 ,decoration: 
          BoxDecoration(border: Border.all()), 
          alignment: Alignment.centerLeft,
            child : TextFormField(  keyboardType: TextInputType.numberWithOptions(decimal: true), // Shows numeric keyboard
              inputFormatters: [
                FilteringTextInputFormatter.allow(RegExp(r'^\d+\.?\d{0,2}')),
              ],textAlignVertical: TextAlignVertical.top,
            onChanged: (value) => {minComssion = double.tryParse(value) ?? 0.0,
              widget.onMinComissionChanged(minComssion!),},
            decoration: const InputDecoration(
              border: InputBorder.none,
              contentPadding: EdgeInsets.symmetric(horizontal: 2, vertical: -16),
            ),)),
      ]),
      SizedBox(height: 10),
      Row(children:[
        SizedBox(width: 120,
        child:  Text('Comission factor:'),
        ),
        Container(width: 200, height: 30 ,decoration: 
          BoxDecoration(border: Border.all()), 
          alignment: Alignment.centerLeft,
            child : TextField(  keyboardType: TextInputType.numberWithOptions(decimal: true), // Shows numeric keyboard
              inputFormatters: [
                FilteringTextInputFormatter.allow(RegExp(r'^0\.?\d{0,4}')),
              ],textAlignVertical: TextAlignVertical.top,
            onChanged: (value) => {comissionFactor = double.tryParse(value) ?? 0.0,
              validComissionFator(comissionFactor!) ?
              widget.onComssionFactorChanged(comissionFactor!) : _showError('Comission factor must be between 0 and 1'),},
            decoration: const InputDecoration(
              border: InputBorder.none,
              contentPadding: EdgeInsets.symmetric(horizontal: 2, vertical: -16),
            ),)),
      ]),
      ]);

      
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

