import threading
import sys
import json
import requests
from ecdsa import SigningKey, SECP256k1
import pickle

makeWallet_api = 'https://k5tus24a63.execute-api.us-east-1.amazonaws.com/default'
sendMoney_api = 'https://358i06flg5.execute-api.us-east-1.amazonaws.com/default'
viewChain_api = 'https://xy1vih4cbh.execute-api.us-east-1.amazonaws.com/default'
viewWallet_api = 'https://eobf9rg9jj.execute-api.us-east-1.amazonaws.com/default'

ID = ""

def message(response):
    if response.status_code==200:
        print('Success')
        return True
    else:
        print(response.text)
        return False

def setup():
    global ID
    name = input("Name: ").strip()
    init_balance = input("Initial Deposit: ")
    while True:
        try: 
            int(init_balance.strip())
            break
        except:
            init_balance = input("\nInitial Deposit: ")
    publicKey = SigningKey.generate(curve=SECP256k1)
    privateKey = publicKey.get_verifying_key()
    data = {'name':name, 'balance':init_balance, 'key':(publicKey.to_string()).hex()}
    response = requests.post(makeWallet_api, data = json.dumps(data))
    ID = json.loads(response.text)['body']
    print(type(ID))
    print("Wallet ID: " + ID)
    message(response)
    

def viewWallet():
    data = {'id':ID}
    response = requests.post(viewWallet_api, data = json.dumps(data))
    if message(response):
        ret = json.loads(response.text)['body']
        print(ret)


def viewChain():
    response = requests.get(viewChain_api)
    if message(response):
        ret = json.loads(response.text)['body']
        print(ret)

def send(receiverID, amount, chain):
    data = {"senderID": ID, "receiverID": receiverID, "amount": amount, "number": chain}
    response = requests.post(sendMoney_api, data = json.dumps(data))
    if message(response):
        print("Transaction hash: " + json.loads(response.text)['body'])

def prompt():
    ip = input("What would you like to do?\n").strip()
    if ip=='quit':
        return True
    elif ip=='send':
        address = input("Receiving address: ")
        amount = input("Amount: ")
        chain = input("Chain number:")
        send(address, amount, chain)
    elif ip=='wallet':
        viewWallet()
    elif ip=='chain':
        viewChain()
    else:
        print('Invalid command')
    return False


def main():
    setup()
    while True:
        if prompt():
            break

if __name__ == '__main__':
    main()