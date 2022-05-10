from datetime import datetime
import chainUtil
from transaction import *

class Block:
    def __init__(self, timestamp, lastHash, data, hash):
        self.timestamp = timestamp
        self.lastHash = lastHash
        self.data = data
        self.hash = hash

    def jsonify(self):
        return {'Timestamp':self.timestamp, 'LastHash':self.lastHash, 'Data':self.data, 'Hash':self.hash}

def genesis():
    return Block(0, "gensisLastHash", Transaction(), "genesisHash")
    
def mineBlock(lastBlock, data):
    lastHash = lastBlock.hash
    timestamp = datetime.now()
    msg = f"{timestamp}{lastHash}{data}"
    hash = chainUtil.hash(msg)

    return Block(timestamp, lastHash, data, hash)

def blockHash(block):
    timestamp = block.timestamp
    lastHash = block.lastHash
    data = block.data
    msg = f"{timestamp}{lastHash}{data}"
    return chainUtil.hash(msg)
