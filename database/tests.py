from threading import Thread
from datetime import datetime
from random import randint
from wallet import Wallet, transact

def init(n):
    wallets = {}
    for i in range(n):
        wallets[i] = Wallet(i, balance=10000)
    return wallets


def test1(n):
    wallets = init(10)
    threads = []
    for i in range(n):
        i, j = randint(0,9)
        threads.append(Thread(transact, wallets[i],wallets[j],1))
    
    for t in threads:
        t.start()

def test2(n):
    wallets = init(n)
    threads=[]
    for i in range(100):
        i, j = randint(0,n-1)
        threads.append(Thread(transact, wallets[i],wallets[j],1))
    
    for t in threads:
        t.start()

def main():
    runtimes1 = []
    runtimes2 = []

    for i in range(1000):
        start = datetime.now()
        test1(i)
        end = datetime.now()
        runtimes1.append(end-start)

    for i in range(1000):
        start = datetime.now()
        test2(i)
        end = datetime.now()
        runtimes2.append(end-start)

    return runtimes1, runtimes2








