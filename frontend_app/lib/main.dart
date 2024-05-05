import 'package:camera/camera.dart';
import 'package:flutter/material.dart';
import 'screen/detection_method_selection.dart'; // Adjust the import path as needed

late List<CameraDescription> cameras;

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  cameras = await availableCameras(); // Initialize the cameras list
  runApp(MyApp(cameras: cameras));
}

class MyApp extends StatelessWidget {
  final List<CameraDescription> cameras;

  const MyApp({Key? key, required this.cameras}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: DetectionMethodSelection(cameras: cameras),
    );
  }
}
