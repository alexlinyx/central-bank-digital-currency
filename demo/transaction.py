import chainUtil
from datetime import datetime
import wallet

class Transaction:
    def __init__(self):
        self.id = chainUtil.generateID()
        self.input = None #{"timestamp": None, "amount": 0, "address": None, "signature": None }
        self.outputs = []

def newTransaction(senderID, recipientID, amount):
    if senderID==recipientID:
        return

    sender_balance = wallet.getBalance(senderID)
    if amount > sender_balance:
        print(f"Amount {amount} exceeds balance {sender_balance}")
        return

    wallet.updateBalance(senderID, sender_balance-amount)
    wallet.updateBalance(recipientID, wallet.getBalance(recipientID)+amount)

    transaction = Transaction()
    transaction.outputs.append({"amount": sender_balance-amount, "address":wallet.getPublicKey(senderID)})
    transaction.outputs.append({"amount":amount, "address":wallet.getPublicKey(recipientID)})

    sig = signTransaction(transaction, senderID)

    return sig

def signTransaction(transaction, senderID):
    sig = chainUtil.hash(transaction.outputs)
    transaction.input = {"timestamp": datetime.now(), "amount": wallet.getBalance(senderID), "address": wallet.getPublicKey(senderID), "signature": sig}
    return transaction
    
def verifyTransaction(transaction):
    return chainUtil.verify(transaction.input['address'], transaction.outputs, transaction.input['signature'])

