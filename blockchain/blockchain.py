from block import *

class Blockchain:
    def __init__(self, chain):
        self.chain = chain
    
    def addBlock(self, data):
        newBlock = mineBlock(self.chain[len(self.chain)-1], data)
        self.chain.append(newBlock)
        return newBlock

def isValidChain(chain):
    if (chain[0].hash != "genesisHash"):
        return False
    
    for i in range(1, len(chain)):
        block = chain[i]
        lastBlock = chain[i-1]
        if (block.lashHash != lastBlock.hash or block.hash != blockHash(block)):
            return False
        
    return True