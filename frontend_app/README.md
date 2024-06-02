# mobile_App
# cross platform

A new Flutter project.

## Getting Started


# Flutter App for Lane Detection

## Overview
This Flutter project demonstrates navigation between different screens, integrating various camera models with a mobile interface. The application leverages the Flutter framework and the camera package to provide real-time camera functionality and displays content from different model outputs.

## Features
- **Camera Integration**: Utilizes the camera package to access camera hardware.
- **Model Visualization**: Allows users to view outputs from different ML models including YOLOP, YOLOPv2, and UNet.
- **Web View**: Integrates web views to display model images from a local server.

## Getting Started
1. **Clone the repository:**
   ```
   git clone https://github.com/KNrodrigo/LaneD-Models-App
   ```
2. **Install dependencies:**
   Navigate to the project directory and run:
   ```
   flutter pub get
   ```
3. **Run the application:**
   Ensure a device, or an emulator, is running and execute:
   ```
   flutter run
   ```

## Key Components
- `main.dart`: The entry point of the application, initializing the camera and running the app.
- `camera_unet.dart`, `camera_yolo.dart`, `camera_yolo_two.dart`: Define the camera interfaces for different models.
- `web_view.dart`: Manages web view screens to display images from models.
- `camera_screen.dart`: Includes the implementation for previewing images captured by the camera.

## Routes
The application defines the following routes:
- `/screen1`: YOLOP camera screen.
- `/screen2`: YOLOPv2 camera screen.
- `/screen3`: UNet camera screen.

## Additional Details
### Image Processing and Preview
- **Image Preview**: Provides functionality to display a captured image on a new screen with an app bar titled "Preview Image".
- **Upload Functionality**: Includes a commented-out function to upload images to a server. This could be utilized to integrate real-time image processing features by sending captured images to a server for analysis.

### UNet Camera Integration
- **Image Capture and Handling**: Facilitates capturing images, with checks to ensure the camera is ready. It integrates error handling for common issues like access denial.
- **Image Upload and Processing**: Implements an `Upload` function to send the captured image to a server configured to receive and process images with the UNet model.

### YOLO Camera Integration
- **Image Capturing**: Features a dedicated button for capturing images, ensuring the camera is ready and not currently taking another picture.
- **Image Upload and Processing**: The `Upload` function sends captured images to a server specifically set up to process images using the YOLO model.

### YOLOv2 Camera Integration
- **Camera Configuration**: Sets up the camera with the highest available resolution and handles lifecycle events.
- **Error Handling**: Implements robust error handling for common camera issues, such as access denial.

### Web View Integration
- **Customizable Web View**: Each instance of `MyWebView` can be customized with a unique title and URL, allowing it to serve various content as needed throughout the app.

## Screenshots
Add screenshots here to show how the app looks and feels in action.

#######################################################################
This project is a starting point for a Flutter application.

A few resources to get you started if this is your first Flutter project:

For help getting started with Flutter development, view the
[online documentation](https://docs.flutter.dev/), which offers tutorials,
samples, guidance on mobile development, and a full API reference.
