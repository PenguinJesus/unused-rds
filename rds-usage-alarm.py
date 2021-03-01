"""RDS-Unused AWS Lambda Function
It will go through the REGION's RDS instances and check on CloudWatch for the unused
instances and send it to an SNS topic.
"""

"""
Things to update/add:
- REGION variable (line 18)
- SNS topic to trigger lambda fucntion
- SNS topic for sending information to admin (topic arn reqiured for line: 66)
- Cloudwatch event to trigger sns on set time intervals
"""


from datetime import datetime, timedelta
import boto3

REGION = 'eu-west-2'
"""str: Region to scan
"""

def lambda_handler(event, context):
    """Entry point for the Lambda function
    """
    # Connecting to AWS and getting all the instances
    client = boto3.client('rds', region_name=REGION)
    all_instances = client.describe_db_instances()
    unused_instances = []



    for instance in all_instances['DBInstances']:
        """Checking for instances with no connections and stop them."""
        client = boto3.client('cloudwatch', region_name=REGION)
        print('cloudwatch')

        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=14)

        # Getting DatabaseConnections metrics for the last 14 days
        connection_statistics = client.get_metric_statistics(
            Namespace='AWS/RDS',
            MetricName='DatabaseConnections',
            Dimensions=[
                {
                    'Name': 'DBInstanceIdentifier',
                    'Value': instance['DBInstanceIdentifier']
                },
            ],
            StartTime=start_date,
            EndTime=end_date,
            Period=86400,
            Statistics=["Maximum"]
        )

        total_connection_count = sum(data_point['Maximum']
                                    for data_point in connection_statistics['Datapoints'])

        if total_connection_count == 0:
            unused_instances.append(instance['DBInstanceIdentifier'])

    # return str(unused_instances)
    """Publish all unused RDS instances to SNS topic"""
    sns_client = boto3.client('sns', region_name=REGION)
    sns_client.publish(
        TopicArn='arn:aws:sns:eu-west-2:119078770656:test',
        Message=str(unused_instances),
        Subject='Unused RDS instances',
    )
