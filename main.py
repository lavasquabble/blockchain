import json
import time


from flask import Flask, request

from pymongo import MongoClient

from merkletree import get_merkle_tree_hash


class Block:

    def __init__(self, index, transactions, timestamp, previous_hash):
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.calculateHash()

    def calculateHash(self):
        obj_dict = {
            'index': self.index,
            'transactions': self.transactions,
            'timestamp': self.timestamp,
            'previous_hash': self.previous_hash,
            'nonce': self.nonce
        }

        block_string = json.dumps(obj_dict, sort_keys=True)
        return get_merkle_tree_hash(block_string)
        # return hashlib.sha256(block_string.encode()).hexdigest()

    def proofOfWork(self, block, difficulty):
        block.nonce = 0
        calculatedHash = block.calculateHash()
        while not calculatedHash.startswith('0' * difficulty):
            block.nonce += 1
            calculatedHash = block.calculateHash()
        return calculatedHash

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


class Blockchain:
    def __init__(self):
        self.raw_transactions = []
        self.chain = [self.createGenesisBlock(0, {}, 0)]
        self.difficulty = 4

    def createGenesisBlock(self, index, transactions, prevoisHash):
        genesis_block = Block(index, transactions, time.time(), prevoisHash)
        return genesis_block

    def getLatestBlock(self):

        return self.chain[-1]

    def is_valid_proof(self, block, block_hash):
        return (block_hash.startswith('0' * self.difficulty) and
                block_hash == block.calculateHash())

    # Responsible for adding a new block to the chain
    def addBlock(self, newBlock):
        previous_hash = self.getLatestBlock().hash
        if previous_hash != newBlock.previous_hash:
            print(f'not a valid_previous_hash {newBlock.previous_hash} != {previous_hash}')
            return False
        # if not self.is_valid_proof(newBlock, newBlock.proofOfWork(newBlock, self.difficulty)):
        #     print(f'not a valid_proof')
        #     return False

        self.chain.append(newBlock)

        with open('data.json') as json_file:
            data = json.load(json_file)

        data.append(newBlock.transactions)

        with open('data.json', 'w') as f:
            json.dump(data, f,
                      ensure_ascii=False, indent=4)

        return True

    # Integrity check
    def isChainValid(self):
        for i in range(1, self.chain.length):
            currentBlock = self.chain[i]
            previousBlock = self.chain[i - 1]

            if currentBlock.hash != currentBlock.calculateHash():
                return False

            if currentBlock.previousHash != previousBlock.calculateHash():
                return False

        return True

    def addNewTransaction(self, transaction):
        self.raw_transactions.append(transaction)




app = Flask(__name__)

blockchain = Blockchain()


@app.route('/', methods=['POST'])
def get_chain():

    req_content = request.json

    chain_data = []

    for i, content in enumerate(req_content):
        print(f'Mining block {i+1}...')
        blockchain.addBlock(blockchain.createGenesisBlock(
            i+1, content, blockchain.getLatestBlock().hash))


    db =  get_database()

    for i, block in enumerate(blockchain.chain):
        if i > 0:
            chain_data.append(block.__dict__)

            save_data(db,  json.loads(json.dumps(block.__dict__)))
    return json.dumps({"length": len(chain_data),
                       "chain": chain_data})

@app.route('/', methods=['GET'])
def welcome():
    return json.dumps({"data": "Welcome"})


def get_database():

    CONNECTION_STRING = "mongodb+srv://admin:umindu12@cluster0.9iwkb.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"

    client = MongoClient(CONNECTION_STRING)
    return client['myFirstDatabase']

def save_data(db, data):
    db.block_chain.insert_one(data)

if __name__ == '__main__':
      app.run(port=5000)
