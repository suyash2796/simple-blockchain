import datetime
import hashlib
import json
from flask import Flask, jsonify

class BlockChain:
    def __init__(self):
        self.chain = []
        self.create_block(proof =1, previous_hash = '0')
        
    def create_block(self, proof, previous_hash):
        block = {'index': len(self.chain)+1,
                 'timestamp': str(datetime.datetime.now()),
                 'proof': proof,
                 'previous_hash': previous_hash}
        self.chain.append(block)
        return block
    
    def get_previous_block(self):
        return self.chain[-1]   
    
    #proof of work -  the problem which is very difficult to solve(for miners)
    # but very easy to verify
    
    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof  = False
        while check_proof is False:
            hash_ops =  hashlib.sha256(str(new_proof**2-previous_proof**2).encode()).hexdigest()
            if hash_ops[:4]=='0000':
                check_proof = True
            else:
                new_proof+=1
        return new_proof
    
    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys = True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    
    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_ops =  hashlib.sha256(str(proof**2-previous_proof**2).encode()).hexdigest()
            if hash_ops[:4] != '0000':
                return False
            previous_block = block
            block_index += 1
        return True

app = Flask(__name__)

## creating blockchain

blockchain =  BlockChain()

## mining a new block
@app.route('/mineblock', methods = ['GET'])
def mine_block():
    previous_block =  blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(proof, previous_hash)
    response = {'messsage': 'congrats on mining the new block!!',
                'index': block['index'],
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'previous_hash':block['previous_hash']
                }
    return jsonify(response), 200

## getting the full blockchain

@app.route('/get_chain', methods = ['GET'])
def get_chain():
    response = {'chain': blockchain.chain,
                'length of chain': len(blockchain.chain)}
    return jsonify(response), 200

@app.route('/is_valid', methods = ['GET'])
def check_valid_chain():
    status = blockchain.is_chain_valid(blockchain.chain)
    response = {'is chain_valid?': status}
    return jsonify(response), 200

## runnng the app
    
app.run(host = '0.0.0.0', port = 5000)
    
    

            

         


