
# Lane Detection and Viewing Service App Project -  Master of Computer Science @ University of Wollongong
This app created using flutter and flask provides an API for uploading images for object detection using YOLOP, YOLOPv2, and UNet models.
As this is integrated with a Flutter app, userrs can easily capture or upload images and videos for processing against these detection models. 
Additionally, the app provides a feature to view the processed images or videos based on the selected model.

This app is generally helpful in reseach and academia purposes enabling students and researchers to use this app and to compare how well
different lane detection models perform with each other. Building with open souce in mind, other contributors can contribute to this app by intergation new 
models, designs and to help improve this applicaiton.


## How it Works 
![Alt Text](app_diagram.jpg)

## Setup
Ideally I reccommed to run this in a Linux enviroment
### Pre-requisites
Here's a general outline of the steps you would need to follow to set up YOLO lane detection using Docker:

Install Docker Desktop or Docker Engine: If you're using Windows, you can install Docker Desktop from the official Docker website. Make sure to enable the necessary virtualization features in your BIOS settings if they're not.

Clone the YOLO lane detection repository: You'll need to clone the repository containing the code for YOLO lane detection. 

Make sure to install Git and Git LFS as prerequisites

### Steps to run

1. Clone the repository:

   git clone https://github.com/KNrodrigo/LaneD-Models-App

2. Run the Docker Containers

   Docker compose up

3. To test we can use Client URL, however there is the sandbox mobile app (APK) for this.

   eg:  curl -X POST -F "file=@example.jpg" http://localhost:5000/detect/model/
   replace model with: yolo, yolo2 and unet.

4. To view the images processed against a certain model:
   

## Endpoints

### Upload Image for Object Detection (YOLO)

- **URL:** `/detect/yolo/`
- **Method:** POST
- **Request Body:** Form-data with a file OR picture taken from the flutter app

### Upload Image for Object Detection (YOLO2)

- **URL:** `/detect/yolo2/`
- **Method:** POST
- **Request Body:** Form-data with a file OR picture taken from the flutter app

### Upload Image for Semantic Segmentation (UNET)

- **URL:** `/detect/unet/`
- **Method:** POST
- **Request Body:** Form-data with a file OR picture taken from the flutter app

### View Processed Images (YOLO)

- **URL:** `/view/yolo/`
- **Method:** GET

### View Processed Images (YOLO2)

- **URL:** `/view/yolo2/`
- **Method:** GET

### View Processed Images (UNET)

- **URL:** `/view/unet/`
- **Method:** GET

## Authors

- **Dai Dong** 
- **Shu-YU**
- **Shazeb Gul** 
- **Sabbir Anwar**
- **Sami** 
- **Nawordth Rodrigo** 

## Examples
![Alt Text](YOLO2_example2vNPS.jpg)


