import boto3
import os

class S3Manager:
    def __init__(self):
        self.s3 = boto3.client('s3')
        self.resource = boto3.resource('s3')
    
    def list_buckets(self):
        """List all S3 buckets"""
        response = self.s3.list_buckets()
        print("Your S3 Buckets:")
        for bucket in response['Buckets']:
            print(f"  - {bucket['Name']}")
    
    def create_bucket(self, bucket_name, region='us-west-2'):
        """Create a new S3 bucket"""
        try:
            if region == 'us-east-1':
                self.s3.create_bucket(Bucket=bucket_name)
            else:
                self.s3.create_bucket(
                    Bucket=bucket_name,
                    CreateBucketConfiguration={'LocationConstraint': region}
                )
            print(f"Created bucket: {bucket_name}")
        except Exception as e:
            print(f"Error creating bucket: {e}")
    
    def upload_file(self, bucket_name, file_path, s3_key=None):
        """Upload a file to S3"""
        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            return
        
        if s3_key is None:
            s3_key = os.path.basename(file_path)
        
        try:
            self.s3.upload_file(file_path, bucket_name, s3_key)
            print(f"Uploaded {file_path} to s3://{bucket_name}/{s3_key}")
        except Exception as e:
            print(f"Upload failed: {e}")
    
    def list_files(self, bucket_name):
        """List files in a bucket"""
        try:
            objects = self.s3.list_objects_v2(Bucket=bucket_name)
            if 'Contents' in objects:
                print(f"Files in {bucket_name}:")
                for obj in objects['Contents']:
                    print(f"  - {obj['Key']} ({obj['Size']} bytes)")
            else:
                print("No files found in bucket")
        except Exception as e:
            print(f"Error listing files: {e}")

# Usage example
if __name__ == "__main__":
    manager = S3Manager()
    bucket_name = 'bucket-name'  
    region = 'us-west-2'
    manager.create_bucket(bucket_name, region)
    
    # manager.list_buckets()

    # Upload a file (create a test.txt file first)
    # manager.upload_file('my-test-bucket-unique-name', 'test.txt')
    
    # List files in bucket
    # manager.list_files('humhealth-client-repository')