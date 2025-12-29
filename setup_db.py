import logging
from helper import get_resource

dynamodb = get_resource('dynamodb')
table = dynamodb.Table('Images')

def create_table():
    try:
        existing_tables = [t.name for t in dynamodb.tables.all()]
        if 'Images' not in existing_tables:
            dynamodb.create_table(
                TableName='Images',
                KeySchema=[
                    {'AttributeName': 'image_id', 'KeyType': 'HASH'}
                ],
                AttributeDefinitions=[
                    {'AttributeName': 'image_id', 'AttributeType': 'S'}
                ],
                ProvisionedThroughput={
                    'ReadCapacityUnits': 5,
                    'WriteCapacityUnits': 5
                }
            )
            logging.info("Table 'Images' created successfully.")
    except Exception as e:
        logging.info(f"Error creating table: {e}")

def create_image_info(image_id, file_name, user_owner):
    try:
        table.put_item(
            Item={
                'image_id': image_id,
                'file_name': file_name,
                'user_owner': user_owner,
                'states': 'uploaded'
            }
        )
        logging.info(f"Image info for {image_id} added successfully.")
    except Exception as e:
        logging.info(f"Error adding image info: {e}")

def get_image_info(image_id):
    try:
        response = table.get_item(Key={'image_id': image_id})
        if 'Item' in response:
            logging.info(f"Image info retrieved: {response['Item']}")
    except Exception as e:
        logging.info(f"Error retrieving image info: {e}")
        return None
            
if __name__ == "__main__":
    create_table()
    create_image_info('img_001', 'test_001.jpg', 'user_123')
    get_image_info('img_001')