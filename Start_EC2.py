import boto3
from botocore.exceptions import ClientError

def start_ec2_instance(instance_id, region_name='us-west-2'):
    try:
        ec2 = boto3.resource('ec2', region_name=region_name)
        instance = ec2.Instance(instance_id)

        print(f"Starting instance {instance_id}...")
        instance.start()
        instance.wait_until_running()

        print(f"Instance {instance_id} is now running.")
        return True

    except ClientError as e:
        print(f"Error starting instance: {e}")
        return False


if __name__ == "__main__":
    instance_id = "i-0f54663de5066d627"
    start_ec2_instance(instance_id)
