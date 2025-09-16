import boto3
import os

def s3_operations():
    try:
        # Specify your region explicitly
        region = 'us-west-2'  # Change this to your preferred region
        s3 = boto3.client('s3', region_name=region)
        
        bucket_name = 'boto3-s3-bucket-upload-test'
        
        # Check if file exists locally
        if not os.path.exists('CloudWatch Dashboards.png'):
            print("Error: File 'CloudWatch Dashboards.png' not found!")
            # Create a dummy file for testing if needed
            with open('CloudWatch Dashboards.png', 'w') as f:
                f.write('test file content')
            print("Created a test file for demonstration")
        
        # Check if bucket already exists
        try:
            s3.head_bucket(Bucket=bucket_name)
            print(f"Bucket '{bucket_name}' already exists")
        except:
            # Create bucket with proper region configuration
            if region == 'us-east-1':
                # us-east-1 doesn't need LocationConstraint
                s3.create_bucket(Bucket=bucket_name)
            else:
                # Other regions require LocationConstraint
                s3.create_bucket(
                    Bucket=bucket_name,
                    CreateBucketConfiguration={
                        'LocationConstraint': region
                    }
                )
            print(f"Created bucket: {bucket_name} in region: {region}")
        
        # Upload file
        s3.upload_file('CloudWatch Dashboards.png', bucket_name, 'CloudWatch_Dashboards.png')
        print("File uploaded successfully!")
        
        # List objects
        objects = s3.list_objects_v2(Bucket=bucket_name)
        print("Objects in bucket:")
        for obj in objects.get('Contents', []):
            print(f"  - {obj['Key']}, Size: {obj['Size']} bytes")
        
        # Generate presigned URL
        url = s3.generate_presigned_url(
            'get_object',
            Params={'Bucket': bucket_name, 'Key': 'CloudWatch_Dashboards.png'},
            ExpiresIn=3600
        )
        print("Presigned URL:", url)
        
    except Exception as e:
        print(f"Error occurred: {str(e)}")

# Call the function
if __name__ == "__main__":
    s3_operations()