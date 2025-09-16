import boto3

def client_vs_resource():
    print("----Low-Level (Clients)----")
    s3_client = boto3.client('s3')
    response = s3_client.list_buckets()
    for bucket in response['Buckets']:
        print(f"{bucket['Name']}")
    
    print("\n\n\n")
    print("----High-Level (Resources)----")
    s3_resource = boto3.resource('s3')
    for bucket in s3_resource.buckets.all():
        print(f"{bucket.name}")

if __name__=="__main__":
    client_vs_resource()