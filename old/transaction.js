const ChainUtil = require("./chain-util");
const mysql = require('mysql');

const Mutex = require('async-mutex').Mutex;

const mutex = new Mutex() // creates a shared mutex instance

class Transaction {
  constructor() {
    this.id = ChainUtil.generateID();
    this.input = { timestamp: 0, amount: 0, address: null, signature: null };
    this.outputs = [{ amount: 0, address: null }];
  }

  static newTransaction(senderWallet, recipient, amount) {
    if (amount > senderWallet.balance) {
      console.log(`Amount ${amount} exceeds balance ${senderWallet.balance}`);
      return;
    }

    const transaction = new this();
    const output = [
      {
        amount: senderWallet.balance - amount,
        address: senderWallet.getPublicKey(),
      },
      { amount: amount, address: recipient },
    ];
    transaction.outputs.push(...output);
    return this.signTransaction(transaction, senderWallet);
  }

  static signTransaction(transaction, senderWallet) {
    transaction.input = {
      timestamp: Date.now(),
      amount: senderWallet.balance,
      address: senderWallet.getPublicKey(),
      signature: senderWallet.sign(ChainUtil.hash(transaction.outputs)),
    };

    return transaction;
  }

  static verifyTransaction(transaction){
    return ChainUtil.verifySignature(transaction.input.address, ChainUtil.hash(transaction.outputs), transaction.input.signature);
  }

}

module.exports = Transaction;
