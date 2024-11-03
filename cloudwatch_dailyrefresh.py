import boto3

# Initialize the boto3 client for EventBridge
client = boto3.client('events')

# Define parameters
rule_name = 'DailyWeatherTrigger'
rule_description = 'Triggers the weather data Lambda function daily at 8 AM UTC'
schedule_expression = 'cron(0 8 * * ? *)'  # Runs daily at 8 AM UTC
lambda_function_arn = 'arn:aws:lambda:REGION:ACCOUNT_ID:function:YourLambdaFunctionName'

# Create or update the rule
response = client.put_rule(
    Name=rule_name,
    ScheduleExpression=schedule_expression,
    State='ENABLED',
    Description=rule_description
)

# Grant EventBridge permission to invoke your Lambda function
lambda_client = boto3.client('lambda')
lambda_client.add_permission(
    FunctionName=lambda_function_arn,
    StatementId='EventBridgeInvokeLambdaPermission',
    Action='lambda:InvokeFunction',
    Principal='events.amazonaws.com',
    SourceArn=response['RuleArn']
)

# Add Lambda function as the target of the rule
client.put_targets(
    Rule=rule_name,
    Targets=[
        {
            'Id': '1',
            'Arn': lambda_function_arn,
        }
    ]
)

print("Scheduled rule created and Lambda target added.")
