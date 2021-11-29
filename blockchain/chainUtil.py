from hashlib import sha256
from uuid import uuid1
from ellipticpy import SigningKey, SECP256k1, BadSignatureError

def generateID():
  return uuid1()

def hash(data):
  h = sha256()
  h.update(str.encode(data))
  return h.hexdigest().decode()

def genPublicKey():
  return SigningKey(curve=SECP256k1)

def getPrivateKey(sk):
  return sk.get_verifying_key()
  
def sign(sk, dataHash):
  return sk.sign(dataHash)
  
def verify(vk, dataHash, signature):
  try:
    return vk.verify(dataHash, signature)
  except BadSignatureError:
    return False