import boto3

def download_s3_file(bucket_name, s3_key, local_path):
    """
    Download a file from Amazon S3 to a local path.
    
    Parameters:
        - bucket_name (str): The name of the S3 bucket.
        - s3_key (str): The key (path) of the file in the S3 bucket.
        - local_path (str): The local path where the file will be saved.
    """
    s3 = boto3.client('s3')
    s3.download_file(bucket_name, s3_key, local_path)

if __name__ == "__main__":
    bucket_name = 'nawordth-rodrigo'
    s3_key = 'input/test.jpg'
    local_path = 'input/test.jpg'
    
    download_s3_file(bucket_name, s3_key, local_path)
