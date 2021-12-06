import chainUtil
from threading import Lock
from datetime import datetime

class Wallet:
  def __init__(self, balance=0):
    self.publicKey = chainUtil.genPublicKey()
    self.privateKey = chainUtil.getPrivateKey(self.publicKey)
    self.balance = balance

  def getPublicKey(self):
    return self.publicKey

  def sign(self, data):
    return chainUtil.sign(self.publicKey, data)

  def calculateBalance(self, blockchain):
    balance = self.balance
    transactions = []

    for block in blockchain.chain:
      transactions.append(block.data)

    walletInputTransactions = [t for t in transactions if t.input and t.input['address']==self.publicKey]
    
    startTime = datetime.min

    if len(walletInputTransactions) > 0:
      for t in walletInputTransactions:
        if t.input and t.input['timestamp']>startTime:
          startTime = t.input['timestamp']
          recentInputTransaction = t
      
      balance = recentInputTransaction.outputs[0]['amount']


    for t in transactions:
      if t.input and t.input['timestamp'] > startTime and t.outputs[1]["address"]==self.publicKey:
        balance += t.outputs[1]['amount']
    
    return balance