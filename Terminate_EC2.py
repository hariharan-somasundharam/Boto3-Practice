import boto3
from botocore.exceptions import ClientError

def terminate_ec2_instance(instance_id, region_name='us-west-2'):
    try:
        ec2 = boto3.resource('ec2', region_name=region_name)
        instance = ec2.Instance(instance_id)

        print(f"Terminating instance {instance_id}...")
        instance.terminate()
        instance.wait_until_terminated()

        print(f"Instance {instance_id} has been terminated.")
        return True

    except ClientError as e:
        print(f"Error terminating instance: {e}")
        return False


if __name__ == "__main__":
    instance_id = "i-0f54663de5066d627"  
    terminate_ec2_instance(instance_id)
