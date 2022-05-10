const Block = require("./block.js");

class Blockchain {
  constructor(chain) {
    this.chain = chain;
  }

  /**
   * Given data, mine a new block with the particular data and push it to the chain
   * @param {string} data
   * @returns {Block}
   */
  addBlock(data) {
    const minedBlock = Block.mineBlock(this.chain[this.chain.length - 1], data);
    this.chain.push(minedBlock);
    return minedBlock;
  }

  /**
   * Given a chain, return true if it is valid, else return false
   * @param {array} chain
   * @returns {boolean}
   */
  isValidChain(chain) {
    //base case
    if (chain[0].hash !== "genesisHash") return false;

    for (let i = 1; i < chain.length; i++) {
      const block = chain[i];
      const lastBlock = chain[i - 1];
      if (block.lastHash !== lastBlock.hash || block.hash !== Block.blockHash(block)){
        return false;
      }
    }
    return true;
  }
}

module.exports = Blockchain;
