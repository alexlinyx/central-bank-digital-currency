from transaction import *
from wallet import *
from blockchain import *

from datetime import datetime
from random import randint
from threading import Thread

def init(n):
    wallets = []
    chains = []
    for i in range(n):
        wallets.append(Wallet(i, balance=1000))
    chains.append(Blockchain())
    return wallets, chains

def send(senderWallet, receipient, chain, amount=1):
    data = newTransaction(senderWallet, receipient, amount)
    chain.addBlock(data)
    

def test1(n):
    wallets, chains = init(10)

    threads = []
    for _ in range(n):
        i, j = randint(0,9), randint(0,9)
        threads.append(Thread(target=send, args=(wallets[i],wallets[j],chains[0],1)))
    
    for t in threads:
        t.start()


def test2(n):
    wallets, chains = init(n)
    
    threads = []
    for _ in range(10):
        i, j = randint(0,n-1), randint(0,n-1)
        threads.append(Thread(target=send, args=(wallets[i],wallets[j],chains[0],1)))
    
    for t in threads:
        t.start()


f1 = open('output3.txt', 'w')
f2 = open('output4.txt', 'w')

for i in range(100):
    start = datetime.now()
    test1(i)
    end = datetime.now()
    diff = (end-start).microseconds
    f1.write(f"{diff}\n")

for i in range(10,100):
    start = datetime.now()
    test2(i)
    end = datetime.now()
    diff = (end-start).microseconds
    f2.write(f"{diff}\n")

f1.close()
f2.close()

