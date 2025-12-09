import 'dart:io';
import 'package:excel/excel.dart';
import 'package:flutter/foundation.dart' show kIsWeb;
import 'backtest_result.dart';
import 'package:universal_html/html.dart' as html;

class ExcelExporter {
  static Future<bool> exportToExcel(List<BacktestResult> data, {String fileName = 'backtest.xlsx'}) async {
    var excel = Excel.createExcel();
    String sheetName = 'Sheet1';
    Sheet sheetObject = excel[sheetName];

    if (data.isEmpty) return false;

    // Add headers
    final statKeys = data.first.statistics.keys.toList();
    List<String> headers = ['Name', 'Balance'];
    headers.addAll(statKeys);
    appendRow(sheetObject, headers);

    // Add data rows
    for (var row in data) {
      final List<dynamic> rowData = [];
      for (var header in headers) {
        if (header == 'Name') {
          rowData.add(row.strategyName.name);
        } else if (header == 'Balance') {
          rowData.add(row.balance);
        } else {
          rowData.add(row.statistics[header] ?? '');
        }
      }
      appendRow(sheetObject, rowData);
    }

   //if (kIsWeb) {
      List<int>? fileBytes = excel.save(fileName:fileName);
      /*if (fileBytes != null) {
        // Create blob
        final blob = html.Blob([fileBytes]);
        
        // Create download link
        final url = html.Url.createObjectUrlFromBlob(blob);
        final anchor = html.AnchorElement(href: url)
          ..setAttribute('download', fileName)
          ..click();
        
        // Cleanup
        html.Url.revokeObjectUrl(url);
      }
    }*/
  return true;
  }

  static Future<bool> exportTransactionsToExcel(List<Transaction> transactions, {String fileName = 'transactions.xlsx'}) async {
    var excel = Excel.createExcel();
    String sheetName = 'Sheet1';
    Sheet sheetObject = excel[sheetName];

    if (transactions.isEmpty) return false;

    // Add headers
    List<String> headers = ['Candle', 'Size', 'Price', 'Commission', 'Profit', 'Balance'];
    appendRow(sheetObject, headers);

    // Add data rows
    for (var tx in transactions) {
      final List<dynamic> rowData = [
        tx.candle,
        tx.size,
        tx.price,
        tx.commission,
        tx.profit,
        tx.balance,
      ];
      appendRow(sheetObject, rowData);

    }

    //if (kIsWeb) {
      List<int>? fileBytes = excel.save(fileName:fileName);
    /*  if (fileBytes != null) {
        // Create blob
        final blob = html.Blob([fileBytes]);
        
        // Create download link
        final url = html.Url.createObjectUrlFromBlob(blob);
        final anchor = html.AnchorElement(href: url)
          ..setAttribute('download', fileName)
          ..click();
        
        // Cleanup
        html.Url.revokeObjectUrl(url);
      }*/

    
   // }
  return true;
  }

  static void appendRow(Sheet sheetObject, List<dynamic> rowData) {
    sheetObject.appendRow(
    rowData.map((value) {
    if (value is int) {
      return IntCellValue(value);
    } else if (value is double) {
      return DoubleCellValue(value);
    } else if (value is bool) {
      return BoolCellValue(value);
    } else {
      return TextCellValue(value.toString());
    }
  }).toList());
  }
  }











