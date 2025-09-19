import boto3

s3 = boto3.resource('s3')
for bucket in s3.buckets.all():
    print(bucket.name)


print("\n")
bucket_name = 'boto3-s3-bucket-upload-test'
bucket = s3.Bucket(bucket_name)
print(bucket.name)
print("\n")

for obj in bucket.objects.all():
    print(obj.key)