from itertools import chain
from backend.blockchain.block3 import Block
from backend.wallet.transaction import Transaction
from backend.config import MINING_REWARD_INPUT
from backend.wallet.wallet import Wallet
'''from module(file) import definition'''

class Blockchain:
    '''
    Blockchain: a public ledger of transactions.
    Inplemented as a list of blocks - data sets of transactions
    '''
    def __init__(self):
        # list of blocks, consist block item that why we want to create a class above the file to represent a block.
        self.chain = [Block.genesis()] # diff from prev, genesis as the first item
        
    def add_block(self, data):
        self.chain.append(Block.mine_block(self.chain[-1], data))

    def __repr__(self):
        '''
        to see the structure in the blockchain that we created(wrapper method)
        '''
        return f'Blockchain: {self.chain}'

    def replace_chain(self, chain):
        '''
        Replace the local chain with the incoming one if the following applies:
        - The incoming chain is longer than the local one.
        - The incoming chain is formatted properly.
        '''
        if len(chain) <= len(self.chain):
            raise Exception('Cannot replace. The incoming chain must be longer.')
        
        try:
            Blockchain.is_valid_chain(chain)
        except Exception as e:
            raise Exception(f'Cannot replace. The incoming chain is invalid: {e}')
        self.chain = chain

    def to_json(self):
        '''
        Serialize the blockchain into a list of blocks
        '''
        return list(map(lambda block: block.to_json(), self.chain))

    @staticmethod
    def from_json(chain_json):
        '''
        Deserialize a list of serialized blocks into a Blockchain instance.
        The result will contain a chain list of Block instances.
        '''
        blockchain = Blockchain()
        blockchain.chain = list(map(lambda block_json: Block.from_json(block_json), chain_json))
        return blockchain

    @staticmethod
    def is_valid_chain(chain):
        '''
        Validate the incoming chain.
        Enforce the following rules of the blockchain:
         - the chain must start with the genesis block
         - blocks must be formatted correctly
        '''
        if chain[0] != Block.genesis():
            raise Exception('The genesis block must be valid')

        for i in range(1, len(chain)):
            block = chain[i]
            last_block = chain[i - 1]
            Block.is_valid_block(last_block, block)
        Blockchain.is_valid_transaction_chain(chain)

    @staticmethod
    def is_valid_transaction_chain(chain):
        '''
        Enforce the rules of a chain composed of blocks of transactions.
            - Each transaction must only appear once in the chain.
            - There can only be one mining reward per block.
            - Each transaction must be valid.
        '''
        transaction_ids = set()

        for i in range(len(chain)):
            block = chain[i]
            has_mining_reward = False

            for transaction_json in block.data:
                transaction = Transaction.from_json(transaction_json)

                if transaction.id in transaction_ids:
                    raise Exception(f'Transaction {transaction.id} is not unique')

                transaction_ids.add(transaction.id)

                if transaction.input == MINING_REWARD_INPUT:
                    if has_mining_reward:
                        raise Exception(
                            'There can only be one mining reward per block.'\
                            f'Check block with hash: {block.hash}'
                        )
                    has_mining_reward = True
                else:
                    historic_blockchain = Blockchain()
                    historic_blockchain.chain = chain[0:i]
                    historic_balance = Wallet.calculate_balance(
                        historic_blockchain,
                        transaction.input['address']
                    )

                    if historic_balance != transaction.input['amount']:
                        raise Exception(
                            f'Transaction {transaction.id} has an invalid '\
                            'input amount'
                    )

                Transaction.is_valid_transaction(transaction)

'''debugging code section'''
def main():
    blockchain = Blockchain()
    blockchain.add_block('one')
    blockchain.add_block('two')
    print(blockchain)
    '''this is a very useful command which allows us to add investigation and debugging code
    to our modules without forcing every file that loades it to also run the same debugging code.'''
    print(f'blockchain.py __name__: {__name__}')

'''now we can take advantage of the name value to control when we'd like to see this main method actually excecute'''
if __name__ == '__main__':
    main()