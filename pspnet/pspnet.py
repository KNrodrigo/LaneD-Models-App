import cv2
import matplotlib.pyplot as plt
import random
from PIL import Image
import tensorflow as tf
import numpy as np
import os
os.environ["SM_FRAMEWORK"] = "tf.keras"

from tensorflow import keras
import segmentation_models as sm


def train_segmentation_model(root_dir, backbone, saved_model_pth, epochs=100):
    train_val_pth = f'{root_dir}\\data\\train.txt'
    test_pth = f'{root_dir}\\data\\test.txt'

    train_val_img_pths = []

    # Open the file in read mode
    with open(train_val_pth, 'r') as file:
        # Read the entire contents of the file into a variable
        file_contents = file.read()
        # train_pths.append(file_contents)
    train_val_img_pths = file_contents.split("\n")

    train_val_img_pths = [pth.strip() for pth in train_val_img_pths]

    # Remove the last item ("Empty string")
    train_val_img_pths = train_val_img_pths[:-1]

    # Create a full path to each training/validation images
    train_val_img_pths = [f'{root_dir}{pth}' for pth in train_val_img_pths]
    train_val_mask_pths = [pth.replace("JPEGImages", "Annotations").replace("jpg", "png") for pth in train_val_img_pths]

    # Zip the lists to map the training/validation original images to their annotations
    combined = list(zip(train_val_img_pths, train_val_mask_pths))

    # Shuffle the combined list
    random.shuffle(combined)

    # Step 3: Unzip the shuffled list back into two lists
    train_img_pths, mask_pths = zip(*combined)  # Unpack the tuples back into separate lists

    # Convert the tuples back to lists (if needed)
    train_val_img_pths = list(train_val_img_pths)
    train_val_mask_pths = list(train_val_mask_pths)

    # Split data into a training and validation set
    VALIDATION_SPLIT = 0.2  # Percentage of data to use for validation

    # Split file paths and labels into training and validation sets
    split_index = int(len(train_val_img_pths) * VALIDATION_SPLIT)
    val_img_pths = train_val_img_pths[:split_index]
    val_mask_pths = train_val_mask_pths[:split_index]
    train_img_pths = train_val_img_pths[split_index:]
    train_mask_pths = train_val_mask_pths[split_index:]

    # Function to resize images and add a batch dimension
    def resize_image(image, target_size=(960, 528)):
        resized_image = tf.image.resize(image, target_size)
        resized_image = tf.expand_dims(resized_image, axis=0)  # Add batch dimension
        return resized_image

    # Function to resize masks and add a batch dimension
    def resize_mask(mask, target_size=(960, 528)):
        resized_mask = tf.image.resize(mask, target_size)
        resized_mask = tf.expand_dims(resized_mask, axis=0)  # Add batch dimension
        return resized_mask

    # Function to load, normalize, and resize images
    def load_image(image_path):
        image = tf.io.read_file(image_path)
        image = tf.image.decode_jpeg(image, channels=3)  # Decode RGB image
        image = tf.image.convert_image_dtype(image, tf.float32)  # Normalize to [0, 1]
        return image

    # Function to load, convert, and resize masks
    def load_mask(mask_path):
        mask = tf.io.read_file(mask_path)
        mask = tf.image.decode_png(mask, channels=1)  # Decode grayscale mask
        mask = tf.where(mask > 0, 1.0, 0.0)  # Convert to binary masks if needed
        return mask

    # Define a function to load, normalize, and resize images and masks
    def load_image_and_mask(image_path, mask_path):
        image = load_image(image_path)
        mask = load_mask(mask_path)

        # Resize images and masks to (960, 528), ensuring batch dimension
        image = resize_image(image)
        mask = resize_mask(mask)

        return image, mask

    # Create a TensorFlow training dataset
    print("=======Create a training dataset!!=======")
    train_dataset = tf.data.Dataset.from_tensor_slices((train_img_pths, train_mask_pths))
    train_dataset = train_dataset.map(load_image_and_mask, num_parallel_calls=tf.data.AUTOTUNE)

    # Create a TensorFlow validation dataset
    print("=======Create a validation dataset!!=======")
    val_dataset = tf.data.Dataset.from_tensor_slices((val_img_pths, val_mask_pths))
    val_dataset = val_dataset.map(load_image_and_mask, num_parallel_calls=tf.data.AUTOTUNE)

    # Choose a backbone from a list of backbones here: https://github.com/qubvel/segmentation_models
    BACKBONE = backbone
    preprocess_input = sm.get_preprocessing(BACKBONE)

    callback = tf.keras.callbacks.EarlyStopping(monitor='loss', patience=3)

    # define model
    model = sm.PSPNet(BACKBONE, input_shape=(960, 528, 3), encoder_weights='imagenet', classes=1, activation='sigmoid')
    model.compile(
        'Adam',
        loss=sm.losses.dice_loss,
        metrics=[sm.metrics.f1_score],
    )

    # fit model
    print("=======Start training model!!=======")
    history = model.fit(
       train_dataset,
       batch_size=100,
       epochs=epochs,
       validation_data=val_dataset,
       callbacks=[callback]
    )

    # Save model
    model.save(saved_model_pth)
    print('=======Model Saved!=======')


    # Evaluate model
    test_img_pths = []

    # Open the file in read mode
    with open(test_pth, 'r') as file:
        # Read the entire contents of the file into a variable
        file_contents = file.read()
        # train_pths.append(file_contents)
    test_img_pths = file_contents.split("\n")

    test_img_pths = test_img_pths[:-1]
    test_img_pths = [pth.strip() for pth in test_img_pths] 

    # Create a full path for each image in the testing set
    test_img_pths = [f'{root_dir}{pth}' for pth in test_img_pths]
    test_mask_pths = [pth.replace("JPEGImages", "Annotations").replace("jpg", "png") for pth in test_img_pths]
    # mask_paths = [f'{ROOT_DIR}/Annotations/{pth.replace("/JPEGImages/", "").replace("jpg", "png")}' for pth in img_pths]

    # Create a TensorFlow dataset
    test_dataset = tf.data.Dataset.from_tensor_slices((test_img_pths, test_mask_pths))
    test_dataset = test_dataset.map(load_image_and_mask)

    # Evaluate the model
    model.evaluate(test_dataset)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Train Segmentation Model')
    parser.add_argument('--root_dir', type=str, help='Root directory')
    parser.add_argument('--backbone', type=str, default='resnet101', help='Backbone')
    parser.add_argument('--saved_model_pth', type=str, default='model.keras', help='Path to save the model')
    parser.add_argument('--epochs', type=int, default=50, help='Number of epochs')

    args = parser.parse_args()
    train_segmentation_model(args.root_dir, args.backbone, args.saved_model_pth, args.epochs)
