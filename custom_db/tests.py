from threading import Thread
from datetime import datetime
from random import randint
from wallet import Wallet, transact

def init(n):
    wallets = {}
    for i in range(n):
        wallets[i] = Wallet(i, 100)
    return wallets


def test1(n):
    wallets = init(10)
    threads = []
    for _ in range(n):
        i, j = randint(0,9), randint(0,9)
        threads.append(Thread(target=transact, args=(wallets[i],wallets[j],1)))
    
    for t in threads:
        t.start()

def test2(n):
    wallets = init(n)
    threads=[]
    for _ in range(100):
        i, j = randint(0,n-1), randint(0,n-1)
        threads.append(Thread(target=transact, args=(wallets[i],wallets[j],1)))
    
    for t in threads:
        t.start()

f1 = open('output1.txt', 'w')
f2 = open('output2.txt', 'w')

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








