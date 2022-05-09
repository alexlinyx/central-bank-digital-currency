import boto3

class System:
    def __init__(self, public_key, private_key):
        self.region = 'us-east-1'

        self.client = boto3.client(
            'dynamodb',
            region_name=region,
            aws_access_key_id=public_key,
            aws_secret_access_key=private_key
            )
        self.dynamodb = boto3.resource(
            'dynamodb',
            region_name=region,
            aws_access_key_id=public_key,
            aws_secret_access_key=private_key,
            )

        self.wallet_table = 

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