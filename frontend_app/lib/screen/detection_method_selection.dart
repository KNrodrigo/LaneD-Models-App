import 'package:flutter/material.dart';
import 'package:camera/camera.dart';
import 'camera_screen.dart';

class DetectionMethodSelection extends StatelessWidget {
  final List<CameraDescription> cameras;

  const DetectionMethodSelection({Key? key, required this.cameras})
      : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("Select Detection Method"),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: <Widget>[
            DetectionMethod(
              name: 'YOLO',
              onPressed: () => navigateToCamera(context, 'YOLO'),
            ),
            DetectionMethod(
              name: 'YOLO2',
              onPressed: () => navigateToCamera(context, 'YOLO2'),
            ),
            DetectionMethod(
              name: 'UNET',
              onPressed: () => navigateToCamera(context, 'UNET'),
            ),
          ],
        ),
      ),
    );
  }

  void navigateToCamera(BuildContext context, String method) {
    Navigator.push(
      context,
      MaterialPageRoute(
        builder: (context) =>
            CameraApp(cameras: cameras, detectionMethod: method),
      ),
    );
  }
}

class DetectionMethod extends StatelessWidget {
  final String name;
  final VoidCallback onPressed;

  const DetectionMethod({Key? key, required this.name, required this.onPressed})
      : super(key: key);

  @override
  Widget build(BuildContext context) {
    return ElevatedButton(
      onPressed: onPressed,
      child: Text(name),
    );
  }
}
