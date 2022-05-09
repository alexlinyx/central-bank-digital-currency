from threading import Lock

class Wallet:
    def __init__(self, id, balance=0):
        self.id = id
        self.balance = balance
        self.lock = Lock()

    def getBalance(self):
        return self.balance

    def updateBalance(self, new_balance):
        self.balance = new_balance

def transact(sender, receipient, amount):
    if sender.id == receipient.id:
        return
    
    lock(sender, receipient)

    if amount > sender.balance:
        print(f"Amount {amount} exceeds balance {sender.balance}")
        unlock(sender, receipient)
        return

    sender.balance -= amount
    receipient.balance += amount

    unlock(sender, receipient)

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


