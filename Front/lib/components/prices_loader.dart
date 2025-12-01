
import 'dart:convert';
import 'dart:io';
import 'package:flutter/material.dart';
import 'package:file_picker/file_picker.dart';
import '../api/api_service.dart';
import 'csv_service.dart';

class PricesLoader extends StatefulWidget {
  final Function(List<Map<String, dynamic>> prices)? onPricesLoaded;
  bool enabled = false;
  


  PricesLoader({super.key, required this.enabled, this.onPricesLoaded});

  @override
  State<PricesLoader> createState() => _PricesLoaderState();
}

class _PricesLoaderState extends State<PricesLoader> {
  String? fileName;
  List<Map<String, dynamic>>? prices;
  @override
  Widget build(BuildContext context) {
    return Row(children: [
      Text('Prices file:  '),
      Container(width: 200,height: 30 ,decoration: BoxDecoration(border: Border.all()),alignment: Alignment.centerLeft, child : 
            Text((fileName ?? ' ' ), style: TextStyle(color : widget.enabled ? Colors.black : Colors.grey,),)
            ),
      IconButton(onPressed: _loadPrices, icon: const Icon(Icons.upload_file))
    ],);
 }


  void _loadPrices() async {
    try{
    FilePickerResult? result = await FilePicker.platform.pickFiles(
      type: FileType.custom,
      allowedExtensions: ['csv'], // specify allowed file extensions
      allowMultiple: false,
      withData: true,
    );

    if (result != null && result.files.single.bytes != null) {
      
      final csvString = utf8.decode(result.files.single.bytes!);
      
      final jsonTable = CsvService.parsePricesCsv(csvString);

      if (jsonTable.isEmpty || jsonTable.length < 2){
        _showError("CSV file is empty or has no data rows.");
        return;
      }
      if (!CsvService.isValidPricesStruct(jsonTable)){
        return;
      }
      setState(() {
        fileName = result.files.single.name;
        prices = jsonTable;
      });
      if (widget.onPricesLoaded != null) {
        widget.onPricesLoaded!(jsonTable);
      }
    }
    } catch(e){
      _showError('Error picking file: $e');
    }
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
