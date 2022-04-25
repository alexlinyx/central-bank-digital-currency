import boto3
import json

with open('../keys.txt') as f:
    public_key = f.readline()
    private_key = f.readline

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
