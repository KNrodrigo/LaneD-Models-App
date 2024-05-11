import 'package:camera/camera.dart';
import 'package:flutter/material.dart';
import 'package:mobile_draft/screen/camera_unet.dart';
import 'dart:convert';
import 'dart:io';

import 'package:mobile_draft/screen/camera_yolo.dart';
import 'package:mobile_draft/screen/camera_yolo_two.dart';
import 'package:mobile_draft/screen/web_view.dart';


late List<CameraDescription> cameras;

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  cameras = await availableCameras();
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter Navigation Example',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: HomeScreen(),
      routes: {
        '/screen1': (context) => YoloCameraApp(),
        '/screen2': (context) => YoloTwoCameraApp(),
        '/screen3': (context) => UnetCameraApp(),
      },
    );
  }
}

class HomeScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Home Screen'),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            ElevatedButton(
              onPressed: () {
                Navigator.pushNamed(context, '/screen1');
              },
              child: const Text('YOLOP Model'),
            ),
            ElevatedButton(
              onPressed: () {
                Navigator.pushNamed(context, '/screen2');
              },
              child: const Text('YOLOPv2 Model'),
            ),
            ElevatedButton(
              onPressed: () {
                Navigator.pushNamed(context, '/screen3');
              },
              child: const Text('UNet Model'),
            ),
            ElevatedButton(
              onPressed: () {
                Navigator.of(context).push(MaterialPageRoute(
                  builder: (BuildContext context) => MyWebView(
                    title: "YOLOP Model Images",
                    selectedUrl: "http://192.168.224.61:5000/view/yolo/",
                  )
                ));
              },
              child: const Text('YOLOP View'),
            ),
            ElevatedButton(
              onPressed: () {
                Navigator.of(context).push(MaterialPageRoute(
                  builder: (BuildContext context) => MyWebView(
                    title: "YOLOPv2 Model Images",
                    selectedUrl: "http://192.168.224.61:5000/view/yolo2/",
                  )
                ));
              },
              child: const Text('YOLOPv2 View'),
            ),
            ElevatedButton(
              onPressed: () {
                Navigator.of(context).push(MaterialPageRoute(
                  builder: (BuildContext context) => MyWebView(
                    title: "UNet Model Images",
                    selectedUrl: "http://192.168.224.61:5000/view/unet/",
                  )
                ));
              },
              child: const Text('UNet View'),
            ),
          ],
        ),
      ),
    );
  }
}
