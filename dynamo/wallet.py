import chainUtil
from datetime import datetime
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
table = dynamodb.Table('Wallets')

class Wallet:
  def __init__(self, id, balance=0):
    self.publicKey = chainUtil.genPublicKey()
    self.privateKey = chainUtil.getPrivateKey(self.publicKey)
    self.id = id

    data = {'Address':id, 'Balance':balance, 'Public Key':self.publicKey, 'NFTs': [], 'COVID Pass': False}
    database.put_item(table, data)

def sign(key, data):
  return chainUtil.sign(key, data)

def getPublicKey(id):
  resp = database.get_item(table, id)
  if resp:
    return resp['Public Key']

def getBalance(id):
  resp = database.get_item(table, id)
  if resp:
    return resp['Balance']

def updateBalance(id, amount):
  database.put_item(table, {"address":id}, "Balance", amount)

