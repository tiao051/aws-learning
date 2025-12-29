import boto3

s3 = boto3.client('s3', endpoint_url='http://localhost:4566')

bucket_name = 'kho-cua-bo'
file_name = 'test_image.jpg'

with open(file_name, "w") as f:
    f.write("Test upload trigger lambda")

try:
    print(f"Processing file '{file_name}' into bucket '{bucket_name}'...")
    s3.upload_file(file_name, bucket_name, file_name)
    print("Upload successful! Lambda will run immediately.")
except Exception as e:
    print(f"Upload error: {e}")