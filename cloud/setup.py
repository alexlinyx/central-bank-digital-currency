import boto3
import json

with open('keys.txt') as f:
    public_key = f.readline().strip()
    private_key = f.readline().strip()

client = boto3.client(
    'dynamodb',
    region_name='us-east-1',
    aws_access_key_id=public_key,
    aws_secret_access_key=private_key
    )
dynamodb = boto3.resource(
    'dynamodb',
    region_name='us-east-1',
    aws_access_key_id=public_key,
    aws_secret_access_key=private_key,
    )
ddb_exceptions = client.exceptions

wallet_table = dynamodb.create_table(
    TableName='users',
    KeySchema=[
        {
            'AttributeName': 'address',
            'KeyType': 'HASH'
        }
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'address',
            'AttributeType': 'S'
        }
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    }
)

chain_table = dynamodb.create_table(
    TableName='chain1',
    KeySchema=[
        {
            'AttributeName': 'sender',
            'KeyType': 'HASH'
        }
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'sender',
            'AttributeType': 'S'
        }
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    }
)