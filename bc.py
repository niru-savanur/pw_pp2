
import datetime


import hashlib

import json




class Blockchain:


    def __init__(self):
        self.chain = []
        self.create_block(proof=1, previous_hash='0', vid="-v1")


    def create_block(self, proof, previous_hash, vid):
        block = {'index': len(self.chain) + 1,
                'timestamp': str(datetime.datetime.now()),
                'proof': proof,
                'previous_hash': previous_hash,
                'vid': vid}
        self.chain.append(block)
        return block


    def print_previous_block(self):
        return self.chain[-1]


    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False

        while check_proof is False:
            hash_operation = hashlib.sha256(
                str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:5] == '00000':
                check_proof = True
            else:
                new_proof += 1

        return new_proof

    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def chain_valid(self):
        previous_block = self.chain[0]
        block_index = 1

        while block_index < len(self.chain):
            self.block = self.chain[block_index]
            if self.block['previous_hash'] != self.hash(previous_block):
                return False

            previous_proof = previous_block['proof']
            proof = self.block['proof']
            hash_operation = hashlib.sha256(
                str(proof**2 - previous_proof**2).encode()).hexdigest()

            if hash_operation[:5] != '00000':
                return False
            previous_block = self.block
            block_index += 1

        return True


    def mine_block(self, vid):
        # previous_block = self.print_previous_block()
        # previous_proof = previous_block['proof']
        # proof = self.proof_of_work(previous_proof)
        # previous_hash = self.hash(previous_block)
        self.create_block(proof=1, previous_hash=self.print_previous_block(), vid=vid)
        return True












