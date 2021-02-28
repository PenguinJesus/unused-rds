# unused-rds
Checking for unused RDS instances (14-days but can be updated in the python script) and sending a message to SNS.

## Prerequisites:
- SNS topic to trigger lambda function
- Cloudwatch event to trigger sns on set time intervals
- SNS topic for sending information to admin



## Things to update/add in script:
- REGION variable (line 18)
- SNS topic for sending information to admin (topic arn reqiured for line: 66)

