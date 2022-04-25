import chainUtil
from threading import Lock
from datetime import datetime

class Wallet:
  def __init__(self, id, balance=0):
    self.publicKey = chainUtil.genPublicKey()
    self.privateKey = chainUtil.getPrivateKey(self.publicKey)
    self.balance = balance
    self.id = id
    self.lock = Lock()

  def getPublicKey(self):
    return self.publicKey

  def sign(self, data):
    return chainUtil.sign(self.publicKey, data)