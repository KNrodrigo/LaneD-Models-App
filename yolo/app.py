from flask import Flask, request, jsonify
import boto3
import subprocess
import os
import random
import string

app = Flask(__name__)

# Configure Boto3 with your AWS credentials
s3 = boto3.client('s3')

@app.route('/detect/', methods=['POST'])
def detect():
    if 'file' not in request.files:
        return jsonify({'error': 'No file found'}), 400
    file = request.files['file']
    file_name = file.filename

    base_name, extension = os.path.splitext(file_name)

    # Generate a random string of length 5
    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=5))

    # Add the random string and the original extension back
    new_file_name = f"{base_name}{random_string}{extension}"
    file_path =new_file_name
    # Save the file locally
    file.save(file_path)

    # Upload the file to S3
    try:
        s3.upload_file(file_path, 'nawordth-rodrigo', "input/" + new_file_name)
    except Exception as e:
        return jsonify({'error': f'Failed to upload file to S3: {str(e)}'}), 500

    try:
        os.remove(file_path)
    except Exception as e:
        # Handle file removal failure
        return jsonify({'error': f'Failed to remove temporary file: {str(e)}'}), 500

    # Call the standalone Python script to process the image/video
    try:
        subprocess.run(['python', 'demo.py', new_file_name])
    except Exception as e:
        # Handle subprocess failure
        return jsonify({'error': f'Failed to execute subprocess: {str(e)}'}), 500

    return jsonify({'message': 'File uploaded and processing started'})

@app.route('/view/', methods=['GET'])
def view():
    # Implement logic to view processed results
    # Retrieve processed results from S3 or any other storage location
    # Return the processed results to the client

    return jsonify({'message': 'Viewing processed results'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
