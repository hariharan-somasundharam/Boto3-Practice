# Fixed Cost Reporter - Correct Calculation
import boto3
import datetime

class SimpleCostReporter:
    def __init__(self):
        self.ce = boto3.client('ce', region_name='us-east-1')
        self.s3 = boto3.client('s3')
    
    def get_cost_data(self, days=7):
        """Get cost data with comprehensive error handling"""
        end_date = datetime.datetime.now().date()
        start_date = end_date - datetime.timedelta(days=days)
        
        try:
            response = self.ce.get_cost_and_usage(
                TimePeriod={'Start': start_date.strftime('%Y-%m-%d'), 
                           'End': end_date.strftime('%Y-%m-%d')},
                Granularity='DAILY',
                Metrics=['UnblendedCost', 'AmortizedCost'],
                GroupBy=[{'Type': 'DIMENSION', 'Key': 'SERVICE'}]
            )
            return response
        except Exception as e:
            print(f"Error fetching cost data: {e}")
            return None
    
    def format_report(self, cost_data):
        """Format cost data as text with correct calculation"""
        if not cost_data or 'ResultsByTime' not in cost_data:
            return "No cost data available\n"
        
        report = "AWS COST BREAKDOWN REPORT\n"
        report += "=" * 50 + "\n\n"
        
        total_cost = 0.0
        
        for day_result in cost_data['ResultsByTime']:
            date = day_result['TimePeriod']['Start']
            
            # Method 1: Try to get daily total from Total section
            daily_total = 0.0
            if 'Total' in day_result and day_result['Total']:
                for metric in ['UnblendedCost', 'AmortizedCost']:
                    if (metric in day_result['Total'] and 
                        'Amount' in day_result['Total'][metric] and
                        day_result['Total'][metric]['Amount']):
                        try:
                            amount_str = day_result['Total'][metric]['Amount']
                            if amount_str and amount_str != '0':
                                daily_total = float(amount_str)
                                break
                        except (ValueError, TypeError) as e:
                            print(f"Error converting amount for {metric}: {e}")
                            continue
            
            # Method 2: If Total section is empty, calculate from services
            if daily_total == 0.0:
                services = day_result.get('Groups', [])
                for service in services:
                    for metric in ['UnblendedCost', 'AmortizedCost']:
                        if metric in service.get('Metrics', {}):
                            try:
                                amount_str = service['Metrics'][metric]['Amount']
                                if amount_str and amount_str != '0':
                                    daily_total += float(amount_str)
                                    break  # Only count each service once
                            except (ValueError, TypeError):
                                continue
            
            total_cost += daily_total
            
            report += f"Date: {date}\n"
            report += f"Total: ${daily_total:.4f}\n"
            report += "Services:\n"
            
            # Calculate daily total from services to verify
            daily_from_services = 0.0
            services = day_result.get('Groups', [])
            if services:
                for service in services:
                    service_name = service['Keys'][0] if service['Keys'] else 'Unknown'
                    service_cost = 0.0
                    
                    for metric in ['UnblendedCost', 'AmortizedCost']:
                        if metric in service.get('Metrics', {}):
                            try:
                                amount_str = service['Metrics'][metric]['Amount']
                                if amount_str and amount_str != '0':
                                    service_cost = float(amount_str)
                                    daily_from_services += service_cost
                                    break
                            except (ValueError, TypeError):
                                continue
                    
                    if service_cost > 0:
                        report += f"  - {service_name}: ${service_cost:.4f}\n"
            else:
                report += "  - No service data\n"
            
            # Add verification line
            report += f"  [Verification: Sum of services: ${daily_from_services:.4f}]\n"
            report += "\n"
        
        report += "=" * 50 + "\n"
        report += f"GRAND TOTAL: ${total_cost:.4f}\n"
        
        return report
    
    def debug_cost_data(self, cost_data):
        """Debug function to see raw cost data structure"""
        if not cost_data:
            return "No cost data available"
        
        debug_info = "DEBUG - RAW COST DATA STRUCTURE\n"
        debug_info += "=" * 60 + "\n"
        
        for i, day_result in enumerate(cost_data.get('ResultsByTime', [])):
            debug_info += f"\nDay {i+1}:\n"
            debug_info += f"Date: {day_result['TimePeriod']['Start']}\n"
            
            # Show Total section correctly
            if 'Total' in day_result:
                debug_info += "Total section:\n"
                for metric, data in day_result['Total'].items():
                    debug_info += f"  {metric}: {data}\n"
            else:
                debug_info += "No Total section found\n"
            
            # Show number of services
            if 'Groups' in day_result and day_result['Groups']:
                debug_info += f"Number of services: {len(day_result['Groups'])}\n"
                # Show first service example
                first_service = day_result['Groups'][0]
                debug_info += f"First service example keys: {first_service.get('Keys', [])}\n"
                debug_info += f"First service example metrics: {first_service.get('Metrics', {})}\n"
            else:
                debug_info += "No service groups found\n"
        
        return debug_info
    
    def save_to_s3(self, report_text, bucket_name, filename_suffix=""):
        """Save report to S3 with error handling"""
        try:
            # Create unique filename
            timestamp = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
            s3_key = f"cost-reports/daily-breakdown-{timestamp}{filename_suffix}.txt"
            
            self.s3.put_object(
                Bucket=bucket_name,
                Key=s3_key,
                Body=report_text.encode('utf-8'),
                ContentType='text/plain'
            )
            
            return f"s3://{bucket_name}/{s3_key}"
            
        except Exception as e:
            print(f"Error saving to S3: {e}")
            return None

def main():
    print("Generating AWS Cost Breakdown...")
    
    reporter = SimpleCostReporter()
    
    # Get cost data
    cost_data = reporter.get_cost_data(days=7)
    
    if not cost_data:
        print("No cost data available or access denied")
        return
    
    # First, let's debug the data structure
    debug_report = reporter.debug_cost_data(cost_data)
    print("\nDebug Information:")
    print("=" * 50)
    print(debug_report)
    
    # Format main report
    report = reporter.format_report(cost_data)
    
    # Save reports to S3
    bucket = "my-cost-reports-2025"
    
    # Save main report
    s3_location = reporter.save_to_s3(report, bucket)
    
    # Save debug report
    debug_location = reporter.save_to_s3(debug_report, bucket, "-debug")
    
    if s3_location:
        print(f"Success! Report saved to: {s3_location}")
        if debug_location:
            print(f"Debug report saved to: {debug_location}")
        
        print("\nReport Content:")
        print("=" * 50)
        print(report)
    else:
        print("Failed to save report to S3")

if __name__ == "__main__":
    main()