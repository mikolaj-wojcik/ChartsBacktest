
import 'dart:convert';
import 'dart:io';
import 'package:flutter/material.dart';
import 'package:file_picker/file_picker.dart';
import '../api/api_service.dart';

class FileLoader extends StatefulWidget {
  final Function(File) onFileSelected;
  final Function(Map<String, dynamic>)? onParametersChanged;
  bool enabled = false;


  FileLoader({super.key, required this.onFileSelected, required this.enabled, this.onParametersChanged});

  @override
  State<FileLoader> createState() => _FileLoaderState();
}

class _FileLoaderState extends State<FileLoader> {
  String? fileName;
  String? strategyName;
  String? code;
  Map<String, dynamic>? parameters;
  bool? validationResult;

  Future<void> _pickFile() async {
    try{
    FilePickerResult? result = await FilePicker.platform.pickFiles(
      type: FileType.custom,
      allowedExtensions: ['py'], // specify allowed file extensions
      allowMultiple: false,
      withData: true,
    );

    if (result != null && result.files.single.bytes != null) {
      //File file = File(result.files.single.path!);
      
      setState(() {
        fileName = result.files.single.name;
        code = base64Encode(result.files.single.bytes!);
        validationResult = null;

      });

      //widget.onFileSelected(file);
    }
    } catch(e){
      print('Error picking file: $e');
    }
  }

  Future<void> _validateFile() async {
    if (strategyName == null || strategyName!.isEmpty){
      strategyName = '';
      //return;
    }
    if (code == null || code!.isEmpty){
      _showError("Please select a strategy file.");
      return;
    }
    setState(() {
      validationResult = null; // Reset validation result while validating
    });
    try{
      var result = await ApiService.validateStrategy(strategyName!, code!);
      if (result != null && result.containsKey('valid')) {
        setState(() {
          validationResult = result['valid'];
        });
      } else {
        _showError("Invalid response from server during validation.");
      }
      if (validationResult == false && result != null && result.containsKey('message')){
        _showError("Validation failed: ${result['message']}");
      }
      if (validationResult == true && result!.containsKey('message')){
        parameters = result['message'];
        if (widget.onParametersChanged != null){
          widget.onParametersChanged!(parameters!);
        }
      }
      else{
        widget.onParametersChanged!({});
      }
      
    } catch(e){
      _showError("Error validating strategy: $e");
    }
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [Row(children:[
        const Text('Strategy name:  '),
        Container(width: 200, height: 30 ,decoration: 
          BoxDecoration(border: Border.all()), 
          alignment: Alignment.centerLeft,
            child : TextField(enabled: widget.enabled,textAlignVertical: TextAlignVertical.top,
            onChanged: (value) => {strategyName = value},
            decoration: const InputDecoration(
              border: InputBorder.none,
              contentPadding: EdgeInsets.symmetric(horizontal: 2, vertical: -16),
            ),)),
      ]),
      Row(
        children: [
          Container(width: 200,height: 30 ,decoration: BoxDecoration(border: Border.all()),alignment: Alignment.centerLeft, child : 
            Text((fileName ?? ' ' ), style: TextStyle(color : widget.enabled ? Colors.black : Colors.grey,),)
            ),
          IconButton(
            onPressed: widget.enabled ? _pickFile : null,
            icon: const Icon(Icons.upload_file),
          ),
          IconButton(
            onPressed: fileName != null && validationResult == null? _validateFile : null,
            icon: Icon(validationResult == null ? Icons.check_box_outline_blank :
                      (validationResult == true ? Icons.check_box : Icons.error), 
                      color: validationResult == null ? Colors.grey : (validationResult == true ? Colors.green : Colors.red)),
          ),    
        ],
      ),

      ]
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
