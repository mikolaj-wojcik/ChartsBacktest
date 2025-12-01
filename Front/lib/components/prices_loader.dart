
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
  OverlayEntry? _overlayEntry;

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        const Text('Prices file:  '),
        MouseRegion(
          onEnter: (_) => _showPreview(),
          onExit: (_) => _hidePreview(),
          child: Container(
            width: 200,
            height: 30,
            decoration: BoxDecoration(border: Border.all()),
            alignment: Alignment.centerLeft,
            padding: const EdgeInsets.symmetric(horizontal: 8),
            child: Text(
              fileName ?? ' ',
              style: TextStyle(
                color: widget.enabled ? Colors.black : Colors.grey,
              ),
              overflow: TextOverflow.ellipsis,
            ),
          ),
        ),
        IconButton(
          onPressed: widget.enabled ? _loadPrices : null,
          icon: const Icon(Icons.upload_file),
        ),
      ],
    );
  }

  void _showPreview() {
    if (prices == null || prices!.isEmpty) return;

    _overlayEntry = OverlayEntry(
      builder: (context) => Positioned(
        top: 150, 
        left: 100,
        child: Material(
          elevation: 8,
          borderRadius: BorderRadius.circular(8),
          child: Container(
            width: 500,
            constraints: const BoxConstraints(maxHeight: 400),
            padding: const EdgeInsets.all(16),
            decoration: BoxDecoration(
              color: Colors.white,
              border: Border.all(color: Colors.grey),
              borderRadius: BorderRadius.circular(8),
            ),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              mainAxisSize: MainAxisSize.min,
              children: [
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Text(
                      'Price Preview (${prices!.length} rows)',
                      style: const TextStyle(
                        fontWeight: FontWeight.bold,
                        fontSize: 16,
                      ),
                    ),
                    IconButton(
                      icon: const Icon(Icons.close, size: 20),
                      onPressed: _hidePreview,
                    ),
                  ],
                ),
                const Divider(),
                Flexible(
                  child: SingleChildScrollView(
                    child: _buildPreviewTable(),
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );

    Overlay.of(context).insert(_overlayEntry!);
  }

  void _hidePreview() {
    _overlayEntry?.remove();
    _overlayEntry = null;
  }

  Widget _buildPreviewTable() {
    int rowsToShow = prices!.length > 5 ? 5 : prices!.length;
    
    return Table(
      border: TableBorder.all(color: Colors.grey[300]!),
      columnWidths: const {
        0: FlexColumnWidth(2),
        1: FlexColumnWidth(1),
        2: FlexColumnWidth(1),
        3: FlexColumnWidth(1),
        4: FlexColumnWidth(1),
        5: FlexColumnWidth(1),
      },
      children: [
        TableRow(
          decoration: BoxDecoration(color: Colors.grey[200]),
          children: const [
            Padding(
              padding: EdgeInsets.all(8.0),
              child: Text('Date', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 12)),
            ),
            Padding(
              padding: EdgeInsets.all(8.0),
              child: Text('Open', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 12)),
            ),
            Padding(
              padding: EdgeInsets.all(8.0),
              child: Text('High', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 12)),
            ),
            Padding(
              padding: EdgeInsets.all(8.0),
              child: Text('Low', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 12)),
            ),
            Padding(
              padding: EdgeInsets.all(8.0),
              child: Text('Close', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 12)),
            ),
            Padding(
              padding: EdgeInsets.all(8.0),
              child: Text('Volume', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 12)),
            ),
          ],
        ),
        ...prices!.sublist(0, rowsToShow).map((row) {
          return TableRow(
            children: [
              Padding(
                padding: const EdgeInsets.all(8.0),
                child: Text(row['date']?.toString() ?? '-', style: const TextStyle(fontSize: 11)),
              ),
              Padding(
                padding: const EdgeInsets.all(8.0),
                child: Text(_formatNumber(row['open']), style: const TextStyle(fontSize: 11)),
              ),
              Padding(
                padding: const EdgeInsets.all(8.0),
                child: Text(_formatNumber(row['high']), style: const TextStyle(fontSize: 11)),
              ),
              Padding(
                padding: const EdgeInsets.all(8.0),
                child: Text(_formatNumber(row['low']), style: const TextStyle(fontSize: 11)),
              ),
              Padding(
                padding: const EdgeInsets.all(8.0),
                child: Text(_formatNumber(row['close']), style: const TextStyle(fontSize: 11)),
              ),
              Padding(
                padding: const EdgeInsets.all(8.0),
                child: Text(_formatNumber(row['volume']), style: const TextStyle(fontSize: 11)),
              ),
            ],
          );
        }).toList(),
      ],
    );
  }

  String _formatNumber(dynamic value) {
    if (value == null) return '-';
    if (value is num) return value.toStringAsFixed(2);
    return value.toString();
  }

  @override
  void dispose() {
    _hidePreview();
    super.dispose();
  }

  // ... rest of your code


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
