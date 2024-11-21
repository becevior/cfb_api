import boto3
from botocore.exceptions import ClientError

def get_s3_client():
    """Initialize and return an S3 client using environment variables for credentials."""
    return boto3.client('s3')

def get_image(bucket_name, object_key):
    """
    Retrieve an image from an S3 bucket.
    
    Args:
        bucket_name (str): Name of the S3 bucket
        object_key (str): Path to the object in the bucket
        
    Returns:
        tuple: (image_data, content_type)
        
    Raises:
        ClientError: If there's an error accessing the S3 bucket or object
    """
    s3_client = get_s3_client()
    
    try:
        response = s3_client.get_object(Bucket=bucket_name, Key=object_key)
        return response['Body'].read(), response['ContentType']
    except ClientError as e:
        error_code = e.response.get('Error', {}).get('Code', 'Unknown')
        if error_code == 'NoSuchKey':
            raise FileNotFoundError(f"Image not found: {object_key}")
        elif error_code == 'NoSuchBucket':
            raise FileNotFoundError(f"Bucket not found: {bucket_name}")
        elif error_code == 'AccessDenied':
            raise PermissionError("Access denied to S3 resource")
        raise
