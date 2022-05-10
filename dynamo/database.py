import boto3
from boto3.dynamodb.conditions import Key

class Database:
    def __init__(self) -> None:
        with open('keys.txt') as f:
            self.public_key = f.readline().strip()
            self.private_key = f.readline().strip()
        
        self.region = 'us-east-1'
        self.client = boto3.client(
            'dynamodb',
            region_name=self.region,
            aws_access_key_id=self.public_key,
            aws_secret_access_key=self.private_key
            )

        self.dynamodb = boto3.resource(
            'dynamodb',
            region_name=self.region,
            aws_access_key_id=self.public_key,
            aws_secret_access_key=self.private_key,
            )

    def create_table(self, tablename, keyname, capacity=1):
        table = self.dynamodb.create_table(
            TableName=tablename,
            KeySchema=[
                {
                    'AttributeName': keyname,
                    'KeyType': 'HASH'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': keyname,
                    'AttributeType': 'S'
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': capacity,
                'WriteCapacityUnits': capacity
            }
        )
        return table

def get_item(table, key):
    resp = table.get_item(Key=key)
    if 'Item' in resp:
        return resp['Item']
    return None

def put_item(table, data):
    table.put_item(Item=data)

def update_item(table, key, field, val):
    table.update_item(
        Key=key,
        UpdateExpression="set " + field + " = :g",
        ExpressionAttributeValues={
            ':g': val
        }
    )

def delete_item(table, key):
    table.delete_item(Key=key)

def get_all(table, key):
    return table.scan(ProjectionExpression=key)

def cleanup(table, key):
    resp = get_all(table, key)
    for entry in resp['Items']:
        delete_item(table, entry)

def delete_table(table):
    table.delete()
    

    