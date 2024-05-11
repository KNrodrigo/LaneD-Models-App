import 'dart:io';
import 'package:camera/camera.dart';
import 'package:flutter/material.dart';
import 'package:mobile_draft/main.dart';
import 'package:mobile_draft/screen/camera_screen.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:path/path.dart';
import 'package:async/async.dart';

class YoloCameraApp extends StatefulWidget {
  const YoloCameraApp({super.key});
  

  @override
  State<YoloCameraApp> createState() => _YoloCameraAppState();
}

class _YoloCameraAppState extends State<YoloCameraApp> {
  late CameraController _controller;
  @override
  void initState() {
    // TODO: implement initState
    super.initState();
    _controller = CameraController(cameras[0], ResolutionPreset.max);
    _controller.initialize().then((_){
      if(!mounted){
        return;
      }
      setState(() {
        
      });
    }).catchError((Object e) {
      if(e is CameraException){
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
      body: Stack(children: [
        Container(
          height: double.infinity,
          child:CameraPreview(_controller)
          ),
          //button to take picture
          Column(
            mainAxisAlignment: MainAxisAlignment.end,
            crossAxisAlignment: CrossAxisAlignment.center,
            children: [
              Center(
                child: Container(
                  margin: EdgeInsets.all(20.0),
                  child: MaterialButton(
                      onPressed: () async {
                        if(!_controller.value.isInitialized){
                          return null;
                        }
                        if(_controller.value.isTakingPicture){
                          return null;
                        }

                        try {
                          await _controller.setFlashMode(FlashMode.auto);
                          XFile file = await _controller.takePicture();
                          File picture = File(file.path);
                          Upload(picture);

                          
                          // another screen to preview image
                          Navigator.push(
                            context, 
                            MaterialPageRoute(
                              builder: (context) => ImagePreview(file)));
                        } on CameraException catch (e){
                          debugPrint("Error occured while taking picture: $e");
                          return null;
                        }
                      },
                      color: Colors.white,
                      child: const Text("Take a picture"),
                    ),
                ),
              )
            ],
          )
      ]),
    );
  }
}

Upload(File imageFile) async {    
    var stream = http.ByteStream(DelegatingStream.typed(imageFile.openRead()));
      var length = await imageFile.length();

      var uri = Uri.parse('http://192.168.224.61:5000/detect/yolo/');

     var request = http.MultipartRequest("POST", uri);
      var multipartFile = http.MultipartFile('file', stream, length,
          filename: basename(imageFile.path));
          //contentType: new MediaType('image', 'png'));

      request.files.add(multipartFile);
      var response = await request.send();
      print(response.statusCode);
      response.stream.transform(utf8.decoder).listen((value) {
        print(value);
      });
    }