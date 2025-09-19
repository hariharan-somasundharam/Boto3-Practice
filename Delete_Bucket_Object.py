import boto3

S3 = boto3.resource('s3')
def delete_bucket_object(bucket_name, file_name):
    S3.Object(bucket_name, file_name).delete()

bucket_name = "boto3-s3-bucket-upload-test"
file_name = "CloudWatch_Dashboards.png"
delete_bucket_object(bucket_name, file_name)