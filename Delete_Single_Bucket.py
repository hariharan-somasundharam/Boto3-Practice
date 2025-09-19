import boto3

S3 = boto3.resource('s3')
S3.Bucket('boto3-s3-bucket-upload-test').delete()