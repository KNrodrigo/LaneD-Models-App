from flask import Flask, request, jsonify, render_template
import boto3
import subprocess
import os
import random
import string
import requests


app = Flask(__name__)
s3 = boto3.client('s3') #Setting up s3 client in boto3 library

############################################################################################################
#                                                YOLO                                                      #
#                                                                                                          #
############################################################################################################
@app.route('/detect/yolo/', methods=['POST'])
def detect_yolo():
    # Checking if file is sent in client request
   # print('Request body is: {0}'.format(request_body.decode('utf-8'))) 
    if 'file' not in request.files:
        return jsonify({'error': 'No file found'}), 400
    file = request.files['file']
    file_name = file.filename

    # Renaming the file name to make sure its unique, i have also added a prefix based on the model to the file name
    base_name, extension = os.path.splitext(file_name)
    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=5))
    new_file_name = f"YOLO_{base_name}{random_string}{extension}"
    file_path =new_file_name
    file.save(file_path) # Save the file locally

    # Upload the file to S3 for low cost storage
    try:
        s3.upload_file(file_path, 'nawordth-rodrigo', "input/" + new_file_name)
    except Exception as e:
        return jsonify({'error': f'Failed to upload file to S3: {str(e)}'}), 500
    
    # Once uploaded to s3, the file is removed from the current dir
    try:
        os.remove(file_path)
    except Exception as e:
        return jsonify({'error': f'Failed to remove temporary file: {str(e)}'}), 500

    # Only send the file name in the request to the model, since the model downloads the file from s3
    # Send a POST request to the server with the file name in the JSON payload
    data = {'file_name': new_file_name}
    try:
        response = requests.post('http://yolo-svc:5000/', json=data)
        if response.status_code == 200:
              return jsonify({'message': 'File succesfully uploaded and processing started', 'file_name_processed': new_file_name})
        else:
            return jsonify({'error': 'Failed to start processing'}), 500
    except Exception as e:
        return jsonify({'error': f'Failed to send request: {str(e)}'}), 500

############################################################################################################
#                                                YOLO2                                                     #
#                                                                                                          #
############################################################################################################
@app.route('/detect/yolo2/', methods=['POST'])
def detect_yolo2():
    # Checking if file is sent in client request
    if 'file' not in request.files:
        return jsonify({'error': 'No file found'}), 400
    file = request.files['file']
    file_name = file.filename

    # Renaming the file name to make sure its unique, i have also added a prefix based on the model to the file name
    base_name, extension = os.path.splitext(file_name)
    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=5))
    new_file_name = f"YOLO2_{base_name}{random_string}{extension}"
    file_path =new_file_name
    file.save(file_path)     # Saveing the file locally

     # Upload the file to S3 for low cost storage
    try:
        s3.upload_file(file_path, 'nawordth-rodrigo', "input/" + new_file_name)
    except Exception as e:
        return jsonify({'error': f'Failed to upload file to S3: {str(e)}'}), 500

    # Once uploaded to s3, the file is removed from the current dir
    try:
        os.remove(file_path)
    except Exception as e:
        return jsonify({'error': f'Failed to remove temporary file: {str(e)}'}), 500

    # Only send the file name in the request to the model, since the model downloads the file from s3
    # Send a POST request to the server with the file name in the JSON payload
    data = {'file_name': new_file_name}
    try:
        response = requests.post('http://yolo2-svc:5000/', json=data)
        if response.status_code == 200:
           return jsonify({'message': 'File successfully uploaded and processing started', 'file_name_processed': new_file_name})
        else:
            return jsonify({'error': 'Failed to start processing'}), 500
    except Exception as e:
        return jsonify({'error': f'Failed to send request: {str(e)}'}), 500


############################################################################################################
#                                                UNET                                                      #
#                                                                                                          #
############################################################################################################
@app.route('/detect/unet/', methods=['POST'])
def detect_unet():
    # Checking if file is sent in client request
    if 'file' not in request.files:
        return jsonify({'error': 'No file found'}), 400
    file = request.files['file']
    file_name = file.filename

    # Renaming the file name to make sure its unique, i have also added a prefix based on the model to the file name
    base_name, extension = os.path.splitext(file_name)
    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=5))
    new_file_name = f"UNET_{base_name}{random_string}{extension}"
    file_path =new_file_name
    file.save(file_path)     # Saveing the file locally

     # Upload the file to S3 for low cost storage
    try:
        s3.upload_file(file_path, 'nawordth-rodrigo', "input/" + new_file_name)
    except Exception as e:
        return jsonify({'error': f'Failed to upload file to S3: {str(e)}'}), 500

    # Once uploaded to s3, the file is removed from the current dir
    try:
        os.remove(file_path)
    except Exception as e:
        return jsonify({'error': f'Failed to remove temporary file: {str(e)}'}), 500

    # Only send the file name in the request to the model, since the model downloads the file from s3
    # Send a POST request to the server with the file name in the JSON payload
    data = {'file_name': new_file_name}
    try:
        response = requests.post('http://unet-svc:5000/', json=data)
        if response.status_code == 200:
           return jsonify({'message': 'File successfully uploaded and processing started', 'file_name_processed': new_file_name})
        else:
            return jsonify({'error': 'Failed to start processing'}), 500
    except Exception as e:
        return jsonify({'error': f'Failed to send request: {str(e)}'}), 500



############################################################################################################
#                                               Viewing  YOLO                                              #
#                                                                                                          #
############################################################################################################
@app.route('/view/yolo', methods=['GET'])
def view_yolo():
    # S3 bucket name and folder prefix
    bucket_name = 'nawordth-rodrigo'
    prefix = 'output/'

    # Listign objects in the bucket with the the prefix folder
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
    if 'Contents' not in response:
        return jsonify({'error': 'No files found'}), 404
    else:
        keys = [content['Key'] for content in response['Contents']]
        print(keys)
  # Extract file names that start with 'YOLO'
    yolo_files = []
    for item in keys:
        if item.startswith("output/YOLO_"):
         yolo_files.append(item)
    #if not files:
     #   return render_template('error.html', message='No files processed with model YOLO found'), 404

     # Generate pre-signed s3 URLs for each image
    signed_urls = {}
    for file_name in yolo_files:
        signed_url = s3.generate_presigned_url('get_object', Params={'Bucket': bucket_name, 'Key': file_name}, ExpiresIn=3600)
        signed_urls[file_name] = signed_url

     #FOR TESTINF PURPOSES
    # Generating HTML containing embedded <img> elements with the presigned URL
    if yolo_files:
        html_content = ''
        for file_name, url in signed_urls.items():
            html_content += f'<img src="{url}" alt="{file_name}"><br>'
        return html_content, 200
    else: 
        return jsonify({'error': 'No files found'}), 404

    return jsonify({'files': signed_urls}), 200
    # Render HTML template and pass the signed URLs to it
    #return render_template('view_yolo.html', signed_urls=signed_urls)

############################################################################################################
#                                               Viewing   YOLO2                                            #
#                                                                                                          #
############################################################################################################
@app.route('/view/yolo2', methods=['GET'])
def view_yolo2():
    # S3 bucket name and folder prefix
    bucket_name = 'nawordth-rodrigo'
    prefix = 'output/'

    # List objects in the bucket with the specified prefix
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
    if 'Contents' not in response:
        return jsonify({'error': 'No files found'}), 404
    else:
        keys = [content['Key'] for content in response['Contents']]
        print(keys)
  # Extract file names that start with 'YOLO'
    yolo_files = []
    for item in keys:
        if item.startswith("output/YOLO2_"):
         yolo_files.append(item)
    #if not files:
     #   return render_template('error.html', message='No files processed with model YOLO2 found'), 404

    # Generate pre-signed s3 URLs for each image
    signed_urls = {}
    for file_name in yolo_files:
        signed_url = s3.generate_presigned_url('get_object', Params={'Bucket': bucket_name, 'Key': file_name}, ExpiresIn=3600)
        signed_urls[file_name] = signed_url


     #FOR TESTINF PURPOSES
    # Generating HTML containing embedded <img> elements with the presigned URL
    if yolo_files:
        html_content = ''
        for file_name, url in signed_urls.items():
            html_content += f'<img src="{url}" alt="{file_name}"><br>'
        return html_content, 200
    else: 
        return jsonify({'error': 'No files found'}), 404

    return jsonify({'files': signed_urls}), 200
    # Render HTML template and pass the signed URLs to it
    #return render_template('view_yolo.html', signed_urls=signed_urls)

############################################################################################################
#                                               Viewing   UNET                                             #
#                                                                                                          #
############################################################################################################
@app.route('/view/unet', methods=['GET'])
def view_unet():
    # S3 bucket name and folder prefix
    bucket_name = 'nawordth-rodrigo'
    prefix = 'output/'

    # List objects in the bucket with the specified prefix
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
    if 'Contents' not in response:
        return jsonify({'error': 'No files found'}), 404
    else:
        keys = [content['Key'] for content in response['Contents']]
        print(keys)
  # Extract file names that start with 'YOLO'
    yolo_files = []
    for item in keys:
        if item.startswith("output/UNET_"):
         yolo_files.append(item)
    #if not files:
     #   return render_template('error.html', message='No files processed with model UNET found'), 404

    # Generate pre-signed s3 URLs for each image
    signed_urls = {}
    for file_name in yolo_files:
        signed_url = s3.generate_presigned_url('get_object', Params={'Bucket': bucket_name, 'Key': file_name}, ExpiresIn=3600)
        signed_urls[file_name] = signed_url


    #FOR TESTINF PURPOSES
    # Generating HTML containing embedded <img> elements with the presigned URL
    if yolo_files:
        html_content = ''
        for file_name, url in signed_urls.items():
            html_content += f'<img src="{url}" alt="{file_name}"><br>'
        return html_content, 200
    else: 
        return jsonify({'error': 'No files found'}), 404

    return jsonify({'files': signed_urls}), 200
    # Render HTML template and pass the signed URLs to it
    #return render_template('view_yolo.html', signed_urls=signed_urls)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
