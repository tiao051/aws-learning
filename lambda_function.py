import boto3
import json
import urllib.parse
from datetime import datetime

# Connect to DynamoDB via LocalStack
dynamodb = boto3.resource('dynamodb', 
                          endpoint_url='http://host.docker.internal:4566',
                          region_name='us-east-1')

table = dynamodb.Table('Images')

def lambda_handler(event, context):
    print("Received event:", event)
    
    for record in event['Records']:
        bucket_name = record['s3']['bucket']['name']
        file_name = urllib.parse.unquote_plus(record['s3']['object']['key'])

        print(f"New file uploaded: {file_name} in bucket: {bucket_name}")

        try:
            timestamp = datetime.now().isoformat()
            table.put_item(
                Item={
                    'image_id': file_name,
                    'file_name': file_name,
                    'bucket': bucket_name,
                    'uploaded_at': timestamp,
                    'status': 'processed_by_lambda'
                }
            )
            print(f"Image info for {file_name} added to DynamoDB.")
        except Exception as e:
            print(f"Error adding image info to DynamoDB: {e}")

    return {
        'statusCode': 200,
        'body': json.dumps('Lambda function executed successfully!')
    }