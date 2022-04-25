import boto3
import json

client = boto3.client(
    'dynamodb',
    region_name='us-east-1',
    aws_access_key_id='AKIAZTI3VFEI747SZTGA',
    aws_secret_access_key='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',
    )
dynamodb = boto3.resource(
    'dynamodb',
    region_name='us-east-1',
    aws_access_key_id='AKIAZTI3VFEI747SZTGA',
    aws_secret_access_key='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',
    )
ddb_exceptions = client.exceptions

ddb_table = dynamodb.Table('blockchainDB')


item = {'wallets':'testing'}
ddb_table.put_item(
        Item=item
        )
