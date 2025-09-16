import boto3

s3 = boto3.resource('s3')
for bucket in s3.buckets.all():
    print(bucket.name)


print("\n\n")
bucket = s3.Bucket('boto3-s3-bucket-upload-test')
for obj in bucket.objects.all():
    print(obj.key)