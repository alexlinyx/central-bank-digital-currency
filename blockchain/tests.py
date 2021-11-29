import database
import transaction
import wallet
import blockchain

from datetime import datetime
from random import randint



wallets = {}

def init(n):
    for i in range(n):
        wallets[i] = Wallet(i, balance=10000)

def send(i, j, x):
    # send x amount from i to j
    transact(wallets[i], wallets[j], x)

def test1(n):
    init(10)
    threads = []
    for i in range(n):
        i, j = randint(0,9)
        threads.append(Thread(send, i,j,1))
    
    for t in threads:
        t.start()

def test2(n):
    init(n)
    threads=[]
    for i in range(100):
        i, j = randint(0,n-1)
        threads.append(Thread(send, i,j,1))
    
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

