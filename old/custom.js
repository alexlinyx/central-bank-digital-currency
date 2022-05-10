const Wallet = require("./wallet");
const Transaction = require("./transaction");
const Blockchain = require("./blockchain");
const Block = require("./block");
const mysql = require('mysql');

let conn = mysql.createConnection({
  host: "cbdc.cdrifg1jtm5u.us-east-1.rds.amazonaws.com",
  port: 3306,
  user: "admin",
  password: "password",
  database: "sys"
});

conn.connect();

let chain = [Block.genesis()];
let blockchain = new Blockchain(chain);
let num_wallets = 500;
let num_transactions = 500;

let wallets = []
for (let i=0; i < num_wallets; i++) {
  wallets.push(Wallet());
}

for (let i=0; i < num_transactions; i++) {
  let n = Math.floor(Math.random() * num_wallets);
  let wallet = wallets[n];
  let amount = 50;
  let recipient = 'r3c1p13nt';
  let transaction = Transaction.newTransaction(wallet,recipient,amount);

  let lastHash = blockchain.chain[blockchain.chain.length - 1].hash;
  let timestamp = 0;
  let hash = Block.hash(timestamp, lastHash, transaction);
  let block = Block(timestamp, lastHash, transaction, hash);
  blockchain.addBlock(block);
}