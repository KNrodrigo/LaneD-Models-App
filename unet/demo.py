from flask import Flask, request, jsonify
import torch
import os
from torch.utils.data import Dataset
import cv2
from torch.nn import ConvTranspose2d
from torch.nn import Conv2d
from torch.nn import MaxPool2d
from torch.nn import Module
from torch.nn import ModuleList
from torch.nn import ReLU
from torchvision.transforms import CenterCrop
from torch.nn import functional as F
from torch.nn import BCEWithLogitsLoss
from torch.optim import Adam
from torch.utils.data import DataLoader
from sklearn.model_selection import train_test_split
from torchvision import transforms
from imutils import paths
from tqdm import tqdm
import matplotlib.pyplot as plt
import time
import numpy as np
import boto3



app = Flask(__name__)

#Configuration

# determine the device to be used for training and evaluation
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
# determine if we will be pinning memory during data loading
PIN_MEMORY = True if DEVICE == "cuda" else False

# define the number of channels in the input, number of classes,
# and number of levels in the U-Net model
NUM_CHANNELS = 1
NUM_CLASSES = 1
NUM_LEVELS = 3

# define the input image dimensions
INPUT_IMAGE_WIDTH = 299
INPUT_IMAGE_HEIGHT = 299
# define threshold to filter weak predictions
THRESHOLD = 0.5


#Model Architecture
class Block(Module):
	def __init__(self, inChannels, outChannels):
		super().__init__()
		# store the convolution and RELU layers
		self.conv1 = Conv2d(inChannels, outChannels, 3)
		self.relu = ReLU()
		self.conv2 = Conv2d(outChannels, outChannels, 3)
	def forward(self, x):
		# apply CONV => RELU => CONV block to the inputs and return it
		return self.conv2(self.relu(self.conv1(x)))
    
class Encoder(Module):
	def __init__(self, channels=(3, 16, 32, 64)):
		super().__init__()
		# store the encoder blocks and maxpooling layer
		self.encBlocks = ModuleList(
			[Block(channels[i], channels[i + 1])
			 	for i in range(len(channels) - 1)])
		self.pool = MaxPool2d(2)
	def forward(self, x):
		# initialize an empty list to store the intermediate outputs
		blockOutputs = []
		# loop through the encoder blocks
		for block in self.encBlocks:
			# pass the inputs through the current encoder block, store
			# the outputs, and then apply maxpooling on the output
			x = block(x)
			blockOutputs.append(x)
			x = self.pool(x)
		# return the list containing the intermediate outputs
		return blockOutputs
    
class Decoder(Module):
	def __init__(self, channels=(64, 32, 16)):
		super().__init__()
		# initialize the number of channels, upsampler blocks, and
		# decoder blocks
		self.channels = channels
		self.upconvs = ModuleList(
			[ConvTranspose2d(channels[i], channels[i + 1], 2, 2)
			 	for i in range(len(channels) - 1)])
		self.dec_blocks = ModuleList(
			[Block(channels[i], channels[i + 1])
			 	for i in range(len(channels) - 1)])
	def forward(self, x, encFeatures):
		# loop through the number of channels
		for i in range(len(self.channels) - 1):
			# pass the inputs through the upsampler blocks
			x = self.upconvs[i](x)
			# crop the current features from the encoder blocks,
			# concatenate them with the current upsampled features,
			# and pass the concatenated output through the current
			# decoder block
			encFeat = self.crop(encFeatures[i], x)
			x = torch.cat([x, encFeat], dim=1)
			x = self.dec_blocks[i](x)
		# return the final decoder output
		return x
	def crop(self, encFeatures, x):
		# grab the dimensions of the inputs, and crop the encoder
		# features to match the dimensions
		(_, _, H, W) = x.shape
		encFeatures = CenterCrop([H, W])(encFeatures)
		# return the cropped features
		return encFeatures
    
class UNet(Module):
    def __init__(self, encChannels=(3, 16, 32, 64),
                 decChannels=(64, 32, 16),
                 nbClasses=1, retainDim=True,
                 outSize=(INPUT_IMAGE_HEIGHT, INPUT_IMAGE_WIDTH)):
        super().__init__()
        # initialize the encoder and decoder
        self.encoder = Encoder(encChannels)
        self.decoder = Decoder(decChannels)
        # initialize the regression head and store the class variables
        self.head = Conv2d(decChannels[-1], nbClasses, 1)
        self.retainDim = retainDim
        self.outSize = outSize

    def forward(self, x):
        # grab the features from the encoder
        encFeatures = self.encoder(x)
        # pass the encoder features through decoder making sure that
        # their dimensions are suited for concatenation
        decFeatures = self.decoder(encFeatures[::-1][0],
                                   encFeatures[::-1][1:])
        # pass the decoder features through the regression head to
        # obtain the segmentation mask
        map = self.head(decFeatures)
        # check to see if we are retaining the original output
        # dimensions and if so, then resize the output to match them
        if self.retainDim:
            map = F.interpolate(map, self.outSize)
        # return the segmentation map
        return map
	
def upload_to_s3(file_path, bucket_name, object_name=None):
    # If object_name is not specified, use the file name
    if object_name is None:
        object_name = "output/" +file_path.split("/")[-1]
    # Create an S3 client
    s3 = boto3.client('s3')

    try:
        # Upload the file
        response = s3.upload_file(file_path, bucket_name, object_name)
        print(f"File uploaded successfully to S3 bucket {bucket_name} with key {object_name}")
        return response
    except Exception as e:
        print(f"Error uploading file to S3 bucket {bucket_name}: {e}")
        return e

def make_predictions3(model, image, orig, file_name, bucket_name):
    model.eval()
    # turn off gradient tracking
    with torch.no_grad():
        # orig = image.copy()
        predMask = model(image).squeeze()
        predMask = torch.sigmoid(predMask)
        predMask = predMask.cpu().numpy()
        # filter out the weak predictions and convert them to integers
        predMask = (predMask > THRESHOLD) * 255
        predMask = predMask.astype(np.uint8)
        # prepare a plot for visualization
        prepare_plot(orig, predMask)
        # Save the predicted mask locally
        cv2.imwrite(file_name, predMask)
        # Upload the predicted mask to S3
        upload_to_s3(file_name, bucket_name)


#Display function
def prepare_plot(origImage, predMask):
	# initialize our figure
	figure, ax = plt.subplots(nrows=1, ncols=2, figsize=(10, 10))
	# plot the original image, its mask, and the predicted mask
	ax[0].imshow(origImage)
	#ax[1].imshow(origMask)
	ax[1].imshow(predMask)
	# set the titles of the subplots
	ax[0].set_title("Image")
	#ax[1].set_title("Original Mask")
	ax[1].set_title("Predicted Mask")
	# set the layout of the figure and display it
	figure.tight_layout()
	figure.show()


@app.route('/', methods=['POST'])
def detect_unet():
    # Check if the request has JSON data
    if not request.json or 'file_name' not in request.json:
        return jsonify({'error': 'No JSON data or file name found in the request'}), 400
    # Extract the file name from the JSON data
    file_name = request.json['file_name']
    bucket_name = 'nawordth-rodrigo'
    s3_key = 'input/' + file_name
    s3 = boto3.client('s3')
    s3.download_file(bucket_name, s3_key, file_name)
    
    # Call the main_start function with the extracted file name
    # Update your preprocessing here (call another function for preprocessing as per model requirements)
    # Return the file back here and pass that file name to the main start
    main_start(file_name)
    return jsonify({'message': 'File processing started'})


def main_start(file_name):
	#Loading the model
	MODEL_PATH = r"unet_segmentation3.pth"
	bucket_name = 'nawordth-rodrigo'
	#GPU
	# determine the device to be used for inference / predictions
	DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
	unet = torch.load(MODEL_PATH).to(DEVICE)
	#Loading the image
	path = file_name
	image_3 = cv2.imread(path)
	#Image Pre-processing
	image_3 = cv2.cvtColor(image_3, cv2.COLOR_BGR2RGB)
	image_3 = image_3.astype("float32") / 255.0
	image_3 = cv2.resize(image_3, (299, 299))
	orig = image_3.copy()
	image_3 = np.transpose(image_3, (2, 0, 1))
	image_3 = np.expand_dims(image_3, 0)
	image_3 = torch.from_numpy(image_3).to(DEVICE)
	make_predictions3(unet, image_3, orig, path, bucket_name)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)