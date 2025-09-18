import boto3

# s3 = boto3.resource('s3')
# for bucket in s3.buckets.all():
#     print(bucket.name)


# print("\n")
# bucket_name = 'your-bucket-name'
# bucket = s3.Bucket(bucket_name)
# print(bucket.name)
# print("\n")
# for obj in bucket.objects.all():
#     print(obj.key)

S3 = boto3.client('s3')
bucket_list = S3.list_buckets()
print(bucket_list)