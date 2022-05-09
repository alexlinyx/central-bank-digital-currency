from hashlib import sha256
from uuid import uuid1
from ecdsa import SigningKey, SECP256k1, BadSignatureError
import pickle
import json

def generateID():
  return uuid1()

def hash(data):
  h = sha256()
  m = pickle.dumps(data)
  h.update(m)
  return h.hexdigest()

def genPublicKey():
  return SigningKey.generate(curve=SECP256k1)

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