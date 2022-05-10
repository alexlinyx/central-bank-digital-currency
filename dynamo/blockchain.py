from block import *
from chainUtil import *
import database
import boto3
from boto3.dynamodb.conditions import Key

with open('keys.txt') as f:
    public_key = f.readline().strip()
    private_key = f.readline().strip()

region = 'us-east-1'

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
        database.put_item(table, {'Chain_number':chain_no, 'Data':serialize(self.chain)})

def getLastBlock(table, chain_no):
    resp = database.get_item(table, {'Chain_number':chain_no})
    if resp:
        resp = deserialize(resp)
        return resp['Data'][-1]
    
def addBlock(data, chain_no):
    chain = getChain(table, chain_no)
    last_block = chain[-1]
    new_block = mineBlock(last_block, data)
    chain.append(new_block)
    database.put_item(table, {'Chain_number':chain_no, 'Data':serialize(chain)})
    return new_block

def getChain(table, chain_no):
    resp = database.get_item(table, {'Chain_number':chain_no})
    if resp:
        chain = bytes(resp['Data'])
        #print(type(chain))
        return deserialize(chain)


def isValidChain(chain):
    if (chain[0].hash != "genesisHash"):
        return False
    
    for i in range(1, len(chain)):
        block = chain[i]
        lastBlock = chain[i-1]
        if (block.lashHash != lastBlock.hash or block.hash != blockHash(block)):
            return False
        
    return True