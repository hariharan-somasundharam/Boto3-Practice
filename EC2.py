import boto3

class EC2Manager:
    def __init__(self):
        self.ec2 = boto3.client('ec2')
    
    def list_instances(self):
        """List all EC2 instances"""
        response = self.ec2.describe_instances()
        print("EC2 Instances:")
        
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                state = instance['State']['Name']
                instance_id = instance['InstanceId']
                instance_type = instance['InstanceType']
                
                print(f"  - {instance_id} ({instance_type}) - {state}")
    
    def start_instance(self, instance_id):
        """Start an EC2 instance"""
        try:
            self.ec2.start_instances(InstanceIds=[instance_id])
            print(f"Starting instance: {instance_id}")
        except Exception as e:
            print(f"Error starting instance: {e}")
    
    def stop_instance(self, instance_id):
        """Stop an EC2 instance"""
        try:
            self.ec2.stop_instances(InstanceIds=[instance_id])
            print(f"Stopping instance: {instance_id}")
        except Exception as e:
            print(f"Error stopping instance: {e}")

# Usage
if __name__ == "__main__":
    ec2 = EC2Manager()
    ec2.list_instances()
    # ec2.start_instance('i-0b1c0b4d0a1c95e20')
    # ec2.stop_instance('i-0b1c0b4d0a1c95e20')