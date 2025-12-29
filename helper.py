import boto3

AWS_CONFIG = {
    'endpoint_url': 'http://localhost:4566',
    'region_name': 'us-east-1',
    'aws_access_key_id': 'test',
    'aws_secret_access_key': 'test'
}

def get_client(service_name):
    return boto3.client(service_name, **AWS_CONFIG)

def get_resource(service_name):
    return boto3.resource(service_name, **AWS_CONFIG)

def handle_error(e):
    if hasattr(e, 'response'):
        return e.response['Error']['Message']
    return str(e)