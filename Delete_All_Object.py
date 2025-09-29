import boto3

S3 = boto3.resource('s3')
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

bucket_name = 'bucket-name'
delete_all_objects(bucket_name)