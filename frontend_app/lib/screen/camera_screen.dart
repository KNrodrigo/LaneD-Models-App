import 'dart:convert';
import 'dart:io';

import 'package:camera/camera.dart';
import 'package:dio/dio.dart';
import 'package:flutter/material.dart';
import 'package:path/path.dart';
import 'package:async/async.dart';
import 'package:http/http.dart' as http;

class CameraApp extends StatefulWidget {
  final List<CameraDescription> cameras;
  final String detectionMethod;

  const CameraApp(
      {Key? key, required this.cameras, required this.detectionMethod})
      : super(key: key);

  @override
  _CameraAppState createState() => _CameraAppState();
}

class _CameraAppState extends State<CameraApp> {
  late CameraController _controller;

  @override
  void initState() {
    super.initState();
    _controller = CameraController(widget.cameras[0], ResolutionPreset.max);
    _controller.initialize().then((_) {
      if (!mounted) {
        return;
      }
      setState(() {});
    }).catchError((Object e) {
      if (e is CameraException) {
        switch (e.code) {
          case 'CameraAccessDenied':
            print("Access Denied");
            break;
          default:
            print(e.description);
            break;
        }
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text("Camera - ${widget.detectionMethod}"),
      ),
      body: Stack(
        children: [
          CameraPreview(_controller),
          Column(
            mainAxisAlignment: MainAxisAlignment.end,
            crossAxisAlignment: CrossAxisAlignment.center,
            children: [
              Center(
                child: Container(
                  margin: const EdgeInsets.all(20.0),
                  child: MaterialButton(
                    onPressed: () async {
                      if (!_controller.value.isInitialized) {
                        return;
                      }
                      if (_controller.value.isTakingPicture) {
                        return;
                      }

                      try {
                        await _controller.setFlashMode(FlashMode.auto);
                        XFile file = await _controller.takePicture();

                        Navigator.push(
                          context,
                          MaterialPageRoute(
                            builder: (context) =>
                                ImagePreview(file, widget.detectionMethod),
                          ),
                        );
                      } on CameraException catch (e) {
                        debugPrint("Error occurred while taking picture: $e");
                        return;
                      }
                    },
                    color: Colors.white,
                    child: const Text("Take a picture"),
                  ),
                ),
              )
            ],
          )
        ],
      ),
    );
  }
}

class ImagePreview extends StatefulWidget {
  final XFile file;
  final String detectionMethod;

  ImagePreview(this.file, this.detectionMethod, {super.key});

  @override
  State<ImagePreview> createState() => _ImagePreviewState();
}

class _ImagePreviewState extends State<ImagePreview> {
  String detectionResults = '';

  @override
  void initState() {
    super.initState();
    _uploadAndDetect(widget.file, widget.detectionMethod);
  }

  void _uploadAndDetect(XFile imageFile, String detectionMethod) async {
    var stream = http.ByteStream(
        DelegatingStream.typed(File(imageFile.path).openRead()));
    var length = await File(imageFile.path).length();

    // Adjust endpoint URLs based on detectionMethod
    String detectionUrl;
    switch (detectionMethod) {
      case 'YOLO':
        detectionUrl = 'http://192.168.224.61:5000/detect/yolo/';
        break;
      case 'YOLO2':
        detectionUrl = 'http://192.168.224.61:5000/detect/yolo2/';
        break;
      case 'UNET':
        detectionUrl = 'http://192.168.224.61:5000/detect/unet/';
        break;
      default:
        detectionUrl = '';
    }

    var uri = Uri.parse(detectionUrl);

    var request = http.MultipartRequest("POST", uri);
    var multipartFile = http.MultipartFile(
      'file',
      stream,
      length,
      filename: basename(imageFile.path),
    );

    request.files.add(multipartFile);
    var response = await request.send();
    response.stream.transform(utf8.decoder).listen((value) {
      setState(() {
        detectionResults = value;
      });
      print(value);
    });
  }

  @override
  Widget build(BuildContext context) {
    File picture = File(widget.file.path);
    return Scaffold(
      appBar: AppBar(
        title: Text("Preview Image - ${widget.detectionMethod}"),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Image.file(picture),
            const SizedBox(height: 20),
            Text("Detection Results:"),
            Text(detectionResults.isNotEmpty
                ? detectionResults
                : "No results available"),
          ],
        ),
      ),
    );
  }
}
