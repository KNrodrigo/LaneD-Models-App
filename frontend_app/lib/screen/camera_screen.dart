import 'dart:convert';
import 'dart:io';

import 'package:camera/camera.dart';
import 'package:flutter/material.dart';
import 'package:path/path.dart';
import 'package:async/async.dart';
import 'package:http/http.dart' as http;

class ImagePreview extends StatefulWidget {
  ImagePreview(this.file,{super.key});
  XFile file;

  @override
  State<ImagePreview> createState() => _ImagePreviewState();
}

class _ImagePreviewState extends State<ImagePreview> {
  @override
  Widget build(BuildContext context) {
    File picture = File(widget.file.path);
    // Upload(picture);
    return Scaffold(
      appBar: AppBar(title: Text("Preview Image"),),

      body: Center(
          child: Image.file(picture),
        ),
    );
  }
}

// Upload(File imageFile) async {    
//     var stream = http.ByteStream(DelegatingStream.typed(imageFile.openRead()));
//       var length = await imageFile.length();

//       var uri = Uri.parse('http://192.168.224.61:5000/detect/yolo/');

//      var request = http.MultipartRequest("POST", uri);
//       var multipartFile = http.MultipartFile('file', stream, length,
//           filename: basename(imageFile.path));
//           //contentType: new MediaType('image', 'png'));

//       request.files.add(multipartFile);
//       var response = await request.send();
//       print(response.statusCode);
//       response.stream.transform(utf8.decoder).listen((value) {
//         print(value);
//       });
//     }

