import boto3
def test_connection():
    sts = boto3.client('sts')
    identity = sts.get_caller_identity()
    print("Connection successful!")
    print(f"Account ID: {identity['Account']}")
    print(f"User ARN: {identity['Arn']}")
    print(f"Region: {boto3.Session().region_name}")
    User_name = identity['Arn'].split("/")[-1]
    print(f"User Name:{User_name}")

if __name__ == "__main__":
    test_connection()