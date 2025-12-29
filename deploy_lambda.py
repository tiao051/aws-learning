import zipfile
import os
import time
from helper import get_client, handle_error

# Configure
BUCKET_NAME = 'kho-cua-bo'
FUNCTION_NAME = 'process_image'
ZIP_FILE = 'lambda_function.zip'
SOURCE_FILE = 'lambda_function.py'
ROLE_ARN = 'arn:aws:iam::000000000000:role/lambda-role'

def deploy():
    s3_client = get_client('s3')
    lambda_client = get_client('lambda')

    try:
        lambda_client.delete_function(FunctionName=FUNCTION_NAME)
    except Exception:
        pass

    try:
        s3_client.delete_bucket(Bucket=BUCKET_NAME)
    except Exception:
        pass
    
    # Create bucket agaign
    s3_client.create_bucket(Bucket=BUCKET_NAME)

    # Zip file
    try:
        with zipfile.ZipFile(ZIP_FILE, 'w') as zipf:
            zipf.write(SOURCE_FILE)
    except Exception as e:
        print(f"Error zipping: {e}")
        return
    with open(ZIP_FILE, 'rb') as f:
        zip_content = f.read()

    # Create function
    res = lambda_client.create_function(
        FunctionName=FUNCTION_NAME,
        Runtime='python3.12',
        Role=ROLE_ARN,
        Handler='lambda_function.lambda_handler',
        Code={'ZipFile': zip_content},
        Timeout=30
    )
    function_arn = res['FunctionArn']

    # Grant S3 permission to invoke Lambda
    try:
        lambda_client.add_permission(
            FunctionName=function_arn,   
            StatementId='s3_invoke_permission_v2',
            Action='lambda:InvokeFunction',
            Principal='s3.amazonaws.com',
            SourceArn=f'arn:aws:s3:::{BUCKET_NAME}',
            SourceAccount='000000000000'
        )
    except Exception as e:
        print(f"Warning when grant permission: {e}")

    # Sleep 2 seconds to allow the system to save permissions
    time.sleep(2)

    print("\n--- 4. LINKING ---")
    try:
        s3_client.put_bucket_notification_configuration(
            Bucket=BUCKET_NAME,
            NotificationConfiguration={
                'LambdaFunctionConfigurations': [
                    {
                        'LambdaFunctionArn': function_arn,
                        'Events': ['s3:ObjectCreated:*']
                    }
                ]
            },
            SkipDestinationValidation=True 
        )
        print("S3 has been linked with Lambda.")
    except Exception as e:
        print(f"Error in linking step: {handle_error(e)}")
        
    finally:
        if os.path.exists(ZIP_FILE):
            os.remove(ZIP_FILE)

if __name__ == "__main__":
    deploy()