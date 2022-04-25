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

    lock(senderWallet, recipientWallet)

    if amount > senderWallet.balance:
        print(f"Amount {amount} exceeds balance {senderWallet.balance}")
        unlock(senderWallet, recipientWallet)
        return

    transaction = Transaction()
    transaction.outputs.append({"amount": senderWallet.balance-amount, "address":senderWallet.getPublicKey()})
    transaction.outputs.append({"amount":amount, "address":recipientWallet.getPublicKey()})

    senderWallet.balance -= amount
    recipientWallet.balance += amount
    sig = signTransaction(transaction, senderWallet)

    unlock(senderWallet, recipientWallet)
    return sig

def signTransaction(transaction, senderWallet):
    sig = chainUtil.hash(transaction.outputs)
    transaction.input = {"timestamp": datetime.now(), "amount": senderWallet.balance, "address": senderWallet.getPublicKey(), "signature": sig}
    return transaction
    
def verifyTransaction(transaction):
    return chainUtil.verify(transaction.input['address'], transaction.outputs, transaction.input['signature'])

def lock(wallet1, wallet2):
    if wallet1.id<wallet2.id:
        wallet1.lock.acquire()
        wallet2.lock.acquire()
    else:
        wallet2.lock.acquire()
        wallet1.lock.acquire()

def unlock(wallet1, wallet2):
    if wallet1.id<wallet2.id:
        wallet2.lock.release()
        wallet1.lock.release()
    else:
        wallet1.lock.release()
        wallet2.lock.release()
