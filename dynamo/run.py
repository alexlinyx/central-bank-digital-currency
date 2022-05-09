import boto3
import json

# set up transactions to communicate with the cloud

def create_table(tablename, keyname, database, capacity=1):
    table = database.create_table(
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

def cleanup():
    pass

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

    wallet_table = create_table('wallets', 'address', dynamodb)
    chain_table = create_table('wallets', 'address', dynamodb)


if __name__ == '__main__':
    main()

