import os
import boto3
from botocore.exceptions import ClientError

bucket_name = 'fd531fda-6127-49a9-b6dc-5d1754221ed0-us-east-1'
file_key = 'test.txt'
s3_client = boto3.client('s3')

def s3_read(bucket, key):
    """Read the content of an S3 file."""
    response = s3_client.get_object(Bucket=bucket, Key=key)
    content = response['Body'].read().decode('utf-8')
    return content

def s3_write(content, bucket=bucket_name, key=file_key, append=True, newline=True):
    if newline:
        content = '\n' + content
    if append:
        try:
            current_content = s3_read(bucket, key)
            content = current_content + content
        except ClientError as e:
            if e.response['Error']['Code'] == 'NoSuchKey':
                pass
            else:
                raise
        s3_client.put_object(Bucket=bucket, Key=key, Body=content.encode('utf-8'))

