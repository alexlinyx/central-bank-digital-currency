from transaction import *
from wallet import *
from blockchain import *

from datetime import datetime
from random import randint
from threading import Thread

chain = Blockchain()

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


def init(n):
    wallets = []
    for i in range(n):
        wallets.append(Wallet(i, balance=1000))
    chain = Blockchain()
    return wallets

def send(senderWallet, receipient, amount=1):
    data = newTransaction(senderWallet, receipient, amount)
    chain.addBlock(data)

def test1(n):
    wallets = init(10)

    threads = []
    for _ in range(n):
        i, j = randint(0,9), randint(0,9)
        threads.append(Thread(target=send, args=(wallets[i],wallets[j],1)))
    
    for t in threads:
        t.start()


def test2(n):
    wallets = init(n)
    
    threads = []
    for _ in range(10):
        i, j = randint(0,n-1), randint(0,n-1)
        threads.append(Thread(target=send, args=(wallets[i],wallets[j],1)))
    
    for t in threads:
        t.start()


f1 = open('output1.txt', 'w')
f2 = open('output2.txt', 'w')

for i in range(100):
    start = datetime.now()
    test1(i)
    end = datetime.now()
    diff = (end-start).microseconds
    f1.write(f"{diff}\n")

for i in range(10,100):
    start = datetime.now()
    test2(i)
    end = datetime.now()
    diff = (end-start).microseconds
    f2.write(f"{diff}\n")

f1.close()
f2.close()


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
