import boto3
from datetime import datetime

def cost_monitor():
    try:
        # Use us-east-1 for Cost Explorer
        ce = boto3.client('ce', region_name='us-west-1')
        
        # Get cost for current month
        today = datetime.now()
        first_day = today.replace(day=1)
        
        response = ce.get_cost_and_usage(
            TimePeriod={
                'Start': first_day.strftime('%Y-%m-%d'),
                'End': today.strftime('%Y-%m-%d')
            },
            Granularity='MONTHLY',
            Metrics=['BlendedCost']
        )
        
        cost = float(response['ResultsByTime'][0]['Total']['BlendedCost']['Amount'])
        print(f"Current month cost: ${cost:.2f}")
        
        if cost > 20:  # Your threshold
            sns = boto3.client('sns')
            sns.publish(
                TopicArn='arn:aws:sns:us-west-2:753430224904:Cost-Explorer-Details',
                Message=f'AWS costs exceeded threshold: ${cost:.2f}',
                Subject='AWS Cost Alert'
            )
            print("Alert sent via SNS!")
            
    except Exception as e:
        print(f"Error: {str(e)}")
        # More specific error handling
        if "AccessDeniedException" in str(e):
            print("Please check IAM permissions for Cost Explorer")
        elif "InvalidClientTokenId" in str(e):
            print("AWS credentials are invalid or expired")

# Call the function
if __name__ == "__main__":
    cost_monitor()