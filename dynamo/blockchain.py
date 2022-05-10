from block import *
import database
import boto3
from boto3.dynamodb.conditions import Key

with open('keys.txt') as f:
    public_key = f.readline().strip()
    private_key = f.readline().strip()

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
table = dynamodb.Table('Chains')

class Blockchain:
    def __init__(self, chain_no):
        self.chain = [genesis()]
        database.put_item(table, {'Number':chain_no, 'Data':self.chain})

def getLastBlock(table, chain_no):
    resp = database.get_item(table, {'Number':chain_no})
    if resp:
        return resp['Data'][-1]
    
def addBlock(self, data):
    newBlock = mineBlock(self.chain[len(self.chain)-1], data)
    self.chain.append(newBlock)
    return newBlock

def isValidChain(chain):
    if (chain[0].hash != "genesisHash"):
        return False
    
    for i in range(1, len(chain)):
        block = chain[i]
        lastBlock = chain[i-1]
        if (block.lashHash != lastBlock.hash or block.hash != blockHash(block)):
            return False
        
    return True

#def addBlock(self, )