
import 'dart:io';
import 'package:flutter/material.dart';
import 'package:file_picker/file_picker.dart';

class FileLoader extends StatefulWidget {
  final Function(File) onFileSelected;
  bool enabled = false;

  FileLoader({super.key, required this.onFileSelected, required this.enabled});

  @override
  State<FileLoader> createState() => _FileLoaderState();
}

class _FileLoaderState extends State<FileLoader> {
  String? fileName;
  bool? validationResult = null;

  Future<void> _pickFile() async {
    try{
    FilePickerResult? result = await FilePicker.platform.pickFiles(
      type: FileType.custom,
      allowedExtensions: ['py'], // specify allowed file extensions
    );

    if (result != null && result.files.single.bytes != null) {
      //File file = File(result.files.single.path!);
      print(result.files.single.bytes);
      setState(() {
        fileName = result.files.single.name;
        validationResult = null;
      });

      //widget.onFileSelected(file);
    }
    } catch(e){
      print('Error picking file: $e');
    }
  }

  Future<void> _validateFile() async {
    // Placeholder for actual validation logic
    // Here we just simulate a successful validation after a delay
    await Future.delayed(const Duration(seconds: 1));
    setState(() {
      validationResult = false; // or false based on actual validation
    });
  }

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        Container(width: 200, decoration: BoxDecoration(border: Border.all()), child : Text(fileName ?? ' ')),
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
    );
  }
}