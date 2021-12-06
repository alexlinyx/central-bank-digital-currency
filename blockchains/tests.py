from transaction import *
from wallet import *
from blockchain import *

from datetime import datetime
from random import randint


def init(n):
    wallets = []
    for i in range(n):
        wallets.append(Wallet(1000))
    chain = Blockchain()
    return wallets, chain

def send(chain, senderWallet, receipient, amount=1):
    data = newTransaction(senderWallet, receipient, amount)
    chain.addBlock(data)
    #assert verifyTransaction(data)
    #assert isValidChain(chain.chain)
    return chain

def updateBalance(wallet, chain):
    wallet.balance = wallet.calculateBalance(chain)


def test1(n):
    wallets, chain = init(10)

    for _ in range(n):
        i, j = randint(0,9), randint(0,9)
        chain = send(chain, wallets[i],wallets[j].getPublicKey(), 1)
        updateBalance(wallets[i], chain)
        updateBalance(wallets[j], chain)

def test2(n):
    wallets, chain= init(n)

    for _ in range(10):
        i, j = randint(0,n-1), randint(0,n-1)
        chain = send(chain, wallets[i],wallets[j].getPublicKey(), 1)
        updateBalance(wallets[i], chain)
        updateBalance(wallets[j], chain)

f1 = open('output1.txt', 'w')
f2 = open('output2.txt', 'w')

for i in range(100):
    start = datetime.now()
    test1(i)
    diff = datetime.now()-start
    f1.write(f"{diff.microseconds}\n")

for i in range(10,100):
    start = datetime.now()
    test2(i)
    diff = datetime.now()-start
    f2.write(f"{diff.microseconds}\n")

f1.close()
f2.close()

