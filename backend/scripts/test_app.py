import requests
import time

from backend.wallet.wallet import Wallet
from backend import wallet

BASE_URL = 'http://127.0.0.1:5000'

def get_blockchain():
    return requests.get(f'{BASE_URL}/blockchain').json()

def get_blockchain_mine():
    return requests.get(f'{BASE_URL}/blockchain/mine').json()

def post_wallet_transact(recipient, amount):
    return requests.post(
        f'{BASE_URL}/wallet/transact',
        json = { 'recipient': recipient, 'amount': amount}
    ).json()

def get_wallet_info():
    return requests.get(f'{BASE_URL}/wallet/info').json()

start_blockchain = get_blockchain()
print(f'start_blockchain: {start_blockchain}')

recipient = Wallet().address
post_wallet_transact_1 = post_wallet_transact(recipient, 21)
print(f'\npost_wallet_transact_1: {post_wallet_transact_1}')

time.sleep(1) # garantee the previous transaction has been request.
post_wallet_transact_2 = post_wallet_transact(recipient, 13)
print(f'\npost_wallet_transact_2: {post_wallet_transact_2}')

time.sleep(1) # in order to delay the mine to make sure the transactions above
# have enough time to appear in the transaction pool given the network request to do so.
mined_block = get_blockchain_mine()
print(f'\nmined_block: {mined_block}')

wallet_info = get_wallet_info()
print(f'\nwallet_iinfo: {wallet_info}')