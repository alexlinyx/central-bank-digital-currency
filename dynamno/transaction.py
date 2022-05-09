import chainUtil
from datetime import datetime

class Transaction:
    def __init__(self):
        self.id = chainUtil.generateID()
        self.input = None #{"timestamp": None, "amount": 0, "address": None, "signature": None }
        self.outputs = []

def newTransaction(senderWallet, recipientWallet, amount):
    if senderWallet.id==recipientWallet.id:
        return

    if amount > senderWallet.balance:
        print(f"Amount {amount} exceeds balance {senderWallet.balance}")
        return

    transaction = Transaction()
    transaction.outputs.append({"amount": senderWallet.balance-amount, "address":senderWallet.getPublicKey()})
    transaction.outputs.append({"amount":amount, "address":recipientWallet.getPublicKey()})

    senderWallet.balance -= amount
    recipientWallet.balance += amount
    sig = signTransaction(transaction, senderWallet)

    return sig

def signTransaction(transaction, senderWallet):
    sig = chainUtil.hash(transaction.outputs)
    transaction.input = {"timestamp": datetime.now(), "amount": senderWallet.balance, "address": senderWallet.getPublicKey(), "signature": sig}
    return transaction
    
def verifyTransaction(transaction):
    return chainUtil.verify(transaction.input['address'], transaction.outputs, transaction.input['signature'])

