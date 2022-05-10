import boto3
import json
from boto3.dynamodb.conditions import Key
import block


def cleanup():
    pass

def get_item():
    dynamodb = boto3.resource('dynamodb')
    
    table = dynamodb.Table('wallets')      
    
    resp = table.get_item(
            region='us-east-1',
            Key={
                'address' : 1,
            }
        )
    
    if 'Item' in resp:
        print(resp['Item'])

def main():
    try:
        with open('keys.txt') as f:
            public_key = f.readline().strip()
            private_key = f.readline().strip()
    except:
        print('No keys.txt. Invalid access keys.')
        return

    region = 'us-east-1'

    client = boto3.client(
        'dynamodb',
        region_name=region,
        aws_access_key_id=public_key,
        aws_secret_access_key=private_key
        )
    dynamodb = boto3.resource(
        'dynamodb',
        region_name=region,
        aws_access_key_id=public_key,
        aws_secret_access_key=private_key,
        )
    #ddb_exceptions = client.exceptions

    # table = dynamodb.create_table(
    #         TableName='wallets',
    #         KeySchema=[
    #             {
    #                 'AttributeName': 'address',
    #                 'KeyType': 'HASH'
    #             }
    #         ],
    #         AttributeDefinitions=[
    #             {
    #                 'AttributeName': 'address',
    #                 'AttributeType': 'S'
    #             }
    #         ],
    #         ProvisionedThroughput={
    #             'ReadCapacityUnits': 1,
    #             'WriteCapacityUnits': 1
    #         }
    #     )
    table = dynamodb.Table('wallets')    
    table.put_item(Item={'address':'4', 'amount':50, 'random':block.genesis().jsonify()})
    table.update_item(Key={'address':'4'}, UpdateExpression="set amount = :g", 
            ExpressionAttributeValues={
                ':g': 60
            })
    resp = table.get_item(Key={'address':'4'})
    
    if 'Item' in resp:
        print(resp['Item']['amount'])

    resp = table.scan(ProjectionExpression="address")
    for i in resp['Items']:
        table.delete_item(Key=i)
    #client.put_item(TableName='wallets', Item={'address':'hi', 'amount':0})
    #client.update_item(TableName='wallets', Item={'address':{'S':'2'}})
    #table.delete()
    


if __name__ == '__main__':
    main()