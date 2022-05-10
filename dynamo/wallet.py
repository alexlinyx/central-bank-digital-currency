from itertools import chain
import chainUtil
from datetime import datetime
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
table = dynamodb.Table('Wallets')

class Wallet:
  def __init__(self, id, balance=0):
    self.publicKey = chainUtil.genPublicKey()
    self.privateKey = chainUtil.getPrivateKey(self.publicKey)
    self.id = id

    #print(type(self.publicKey.to_string()))
    data = {'Address':id, 'Balance':balance, 'Public_Key':self.publicKey.to_string()}
    database.put_item(table, data)

def sign(key, data):
  return chainUtil.sign(key, data)

def getPublicKey(id):
  resp = database.get_item(table, {'Address':id})
  if resp:
    sk_string = bytes(resp['Public_Key'])
    #print(type(sk_string))
    return chainUtil.getPublicKey(sk_string)

def getBalance(id):
  resp = database.get_item(table, {'Address':id})
  if resp:
    return resp['Balance']

def updateBalance(id, amount):
  database.update_item(table, {"Address":id}, "Balance", amount)

