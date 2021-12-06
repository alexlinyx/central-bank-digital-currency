from hashlib import sha256
from uuid import uuid1
from ecdsa import SigningKey, SECP256k1, BadSignatureError
import pickle
import json

def genPublicKey():
  return SigningKey.generate(curve=SECP256k1)

def generateID():
  return uuid1()

def hash(data):
  h = sha256()
  h.update(pickle.dumps(data))
  #print(data)
  #print(type(pickle.dumps(data)))
  return h.hexdigest()

def getPrivateKey(sk):
  return sk.get_verifying_key()
  
def sign(sk, data):
  dataHash = hash(data)
  return sk.sign(dataHash)
  
def verify(sk, data, signature):
  vk = getPrivateKey(sk)
  dataHash = hash(data)
  try:
    return vk.verify(dataHash, signature)
  except BadSignatureError:
    return False