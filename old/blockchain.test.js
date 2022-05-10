const Blockchain = require("./blockchain");
const Block = require("./block");
const mysql = require('mysql');

jest.setTimeout(5000);

describe("Blockchain", () => {
  let blockchain, blockchain2, chain;

  let conn = mysql.createConnection({
    host: 'cbdc.cdrifg1jtm5u.us-east-1.rds.amazonaws.com',
    port: 3306,
    user: 'admin',
    password: 'password',
    database: 'sys'
  });
  
  beforeAll(done => {
    chain = [];
    conn.connect((err) => {
      if (err) {
        console.log("error connecting to mysql database");
        return;
      }
    });
    /*var sql = "CREATE TABLE chain (address VARCHAR(255))";
    conn.query(sql, (err, result) => {
      if (err) throw err;
      console.log("Table created");
    });*/

    conn.query('SELECT * FROM chain', (err, rows) => {
      console.log("query");
      if (err) throw err;
      let data = rows.sort((a, b) => {
        console.log("rows sort");
        return a.timestamp - b.timestamp;
      });
      if (data.length !== 0) {
        console.log("yes data");
        console.log(data);
        data.forEach((row) => {
          let block = new Block(row.timestamp, row.lasthash, JSON.parse(row.data), row.hash);
          chain.push(block);
        })
      } else {
        console.log("genesis");
        chain = [Block.genesis()];
      }
      blockchain = new Blockchain(chain);
      done();
    });
  });

  afterAll(() => {
    conn.end();
  });

  it("starts with the genesis block", () => {
    console.log(blockchain.chain[0].hash);
    expect(blockchain.chain[0].hash).toEqual("genesisHash");
  });

  it("adds a new block", () => {
    const data = "foo";
    blockchain.addBlock(data);
    expect(blockchain.chain[blockchain.chain.length - 1].data).toEqual(data);
  });

  it("validates a valid chain", () => {
    expect(blockchain.isValidChain(blockchain.chain)).toBe(true);
  });

  it("custom test case", () => {
    for (let i=0; i<500; i++) {
      blockchain.addBlock(i);
    }
    expect(blockchain.chain[blockchain.chain.length - 1].data).toEqual(499)
  })

});