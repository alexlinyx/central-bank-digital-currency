import chainUtil
from datetime import datetime

class Transaction:
    def __init__(self):
        self.id = chainUtil.generateID()
        self.input = {"timestamp": 0, "amount": 0, "address": None, "signature": None }
        self.outputs = []

def newTransaction(senderWallet, recipient, amount):
    if amount > senderWallet.balance:
        senderWallet.lock.release()
        print(f"Amount {amount} exceeds balance {senderWallet.balance}")

    transaction = Transaction()
    transaction.outputs.append({"amount": senderWallet.balance-amount, "address":senderWallet.getPublicKey()})
    transaction.outputs.append({"amount":amount, "address":recipient})

    sig = signTransaction(transaction, senderWallet)

    return sig

def signTransaction(transaction, senderWallet):
    sig = chainUtil.hash(transaction.outputs)
    transaction.input = {"timestamp": datetime.now(), "amount": senderWallet.balance, "address": senderWallet.getPublicKey(), "signature": sig}
    return transaction
    
def verifyTransaction(transaction):
    return chainUtil.verify(transaction.input['address'], chainUtil.hash(transaction.outputs), transaction.input['signature'])
