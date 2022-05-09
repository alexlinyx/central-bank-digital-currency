const ChainUtil = require("./chain-util");

class Wallet {

  /**
   * Create a new wallet object
   * `const w = new Wallet();` would generate a random key pair
   * `const w2 = new Wallet("....")` would import a key pair with private key
   * @param {string} privateKey
   */
  constructor(privateKey = null) {
    // if privateKey is null, eg if the paramenter is empty
    if (privateKey) {
      this.privateKey = privateKey;
      const key = ChainUtil.keyPairFromPrivate(privateKey);
      this.publicKey = ChainUtil.getPublicKey(key);
      this.keyPair = key;
    } else {
      this.keyPair = ChainUtil.genKeyPair();
      this.publicKey = ChainUtil.getPublicKey(this.keyPair);
      this.privateKey = ChainUtil.getPrivateKey(this.keyPair);
    }

    this.balance = 100;
  }

  getKeyPairJSON() {
    return {
      publicKey: this.publicKey,
      privateKey: this.privateKey
    };
  }

  getPublicKey(){
    return this.publicKey;
  }

  calculateBalance(blockchain) {
    let balance = this.balance;

    // create an array of transactions
    let transactions = [];

    // store all the transactions in the array
    blockchain.chain.forEach(block => {
      transactions.push(block.data);
    });

    // get all the transactions generated by the wallet ie money sent by the wallet
    const walletInputTransactions = transactions.filter(transaction => transaction.input && transaction.input.address === this.publicKey);

    // declare a variable to save the timestamp
    let startTime = 0;

    if (walletInputTransactions.length > 0) {

      // get the latest transaction
      const recentInputTransaction = walletInputTransactions.reduce((prev, current) => prev.input.timestamp > current.input.timestamp ? prev : current);

      // get the outputs of that transactions, its amount will be the money that we would get back
      balance = recentInputTransaction.outputs.find(output => output.address === this.publicKey).amount

      // save the timestamp of the latest transaction made by the wallet
      startTime = recentInputTransaction.input.timestamp
    }

    // get the transactions that were addressed to this wallet ie somebody sent some moeny
    // and add its ouputs.
    // since we save the timestamp we would only add the outputs of the transactions recieved
    // only after the latest transactions made by us
    transactions.forEach(transaction => {
      if (transaction.input && transaction.input.timestamp > startTime) {
        transaction.outputs.find(output => {
          if (output.address === this.publicKey) {
            balance += output.amount;
          }
        })
      }
    })
    return balance;

  }

  sign(data){
    return ChainUtil.sign(this.keyPair, data);
  }
}

module.exports = Wallet;