import boto3
from botocore.exceptions import ClientError

def create_ec2_instance(region_name='us-west-2', instance_type='t2.micro', key_name='Harish-Key', subnet_id=None):
    try:
        ami_id = 'ami-0892d3c7ee96c0bf7'
        ec2 = boto3.resource('ec2', region_name=region_name)

        params = {
            "ImageId": ami_id,
            "MinCount": 1,
            "MaxCount": 1,
            "InstanceType": instance_type,
            "KeyName": key_name,
            "TagSpecifications": [
                {
                    'ResourceType': 'instance',
                    'Tags': [
                        {'Key': 'Name', 'Value': 'Harish-Boto3-Instance'},
                        {'Key': 'Environment', 'Value': 'Development'}
                    ]
                }
            ]
        }

        if subnet_id:
            params["SubnetId"] = subnet_id

        instances = ec2.create_instances(**params)
        instance = instances[0]
        print(f"Instance created with ID: {instance.id}")
        print("Waiting for instance to be running...")

        instance.wait_until_running()
        instance.load()

        print(f"Instance {instance.id} is now running")
        print(f"Public IP: {instance.public_ip_address}")
        print(f"State: {instance.state['Name']}")

        return instance.id

    except ClientError as e:
        print(f"Error creating instance: {e}")
        return None


if __name__ == "__main__":
    instance_id = create_ec2_instance(
        key_name="Harish-Key",
        subnet_id="subnet-032af0fbebb6689d9"
    )
    print(f"Created EC2 Instance ID: {instance_id}")
