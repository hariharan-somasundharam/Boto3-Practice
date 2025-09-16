import boto3
from botocore.exceptions import ClientError

def safe_operation():
    s3 = boto3.client('s3')
    try:
        response = s3.list_objects_v2(Bucket='boto3-s3-bucket-test-upload')
        print("Success!")
    except ClientError as e:
        error_code = e.response['Error']['Code']
        print(f"Error: {error_code}")
        print(f"Message: {e.response['Error']['Message']}")

        if error_code == 'NoSuchBucket':
            print("This bucket doesn't exist!")
        elif error_code == 'AccessDenied':
            print("You don't have permission!")

if __name__ == "__main__":
    safe_operation()