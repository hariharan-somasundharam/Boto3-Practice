import boto3

S3 = boto3.resource('s3')
S3.Bucket('bucket-name').delete()