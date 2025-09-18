import boto3

# 'Session' is used to get the current region of the user/role.
# Session = boto3.session.Session()
# print(Session.region_name)


Session = boto3.session.Session()
S3 = boto3.resource('s3')

# Creating a Simple S3 Bucket.
Current_region = Session.region_name
Bucket_Name = 'prathi-buck-test-18092025'
S3_Bucket = S3.create_bucket(Bucket = Bucket_Name, 
            CreateBucketConfiguration={
                'LocationConstraint': Current_region}
            )
print(S3_Bucket)
for bucket in S3.buckets.all():
    print(bucket.name)



# Uploading file to a bucket 
S3.Bucket('prathi-buck-test-18092025').upload_file(Filename='CloudWatch Dashboards.png', Key='Cloudatch_Dashboards.png')


#  Copying Object between buckets
def copy_bucket_object(from_bucket, to_bucket, file_name):
    copy_source ={
        'Bucket' : from_bucket,
        'Key' : file_name
    }
    S3.Object(to_bucket, file_name).copy(copy_source)


from_bucket = "prathi-buck-test-18092025"
to_bucket = "hari-buck-test-18092025"
file_name = "Cloudatch_Dashboards.png"
copy_bucket_object(from_bucket, to_bucket, file_name)


#  Deleting an Object from Bucket
def delete_bucket_object(bucket_name, file_name):
    S3.Object(bucket_name, file_name).delete()

bucket_name = "prathi-buck-test-18092025"
file_name = "Cloudatch_Dashboards.png"
delete_bucket_object(bucket_name, file_name)



# Deleting Non-empty Buckets
def delete_all_objects(bucket_name):
    res = []
    bucket = S3.Bucket(bucket_name)
    for obj in bucket.object_versions.all():
        res.append({
            'Key' : obj.object_key,
            'VersionId' : obj.id
        })
    print(res)
    bucket.delete_objects(Delete={'Objects' : res})

bucket_name = 'boto3-s3-bucket-upload-test'
delete_all_objects(bucket_name)


# Deleting an Empty Buckets
S3.Bucket('your-bucket-name').delete()
