from solana.rpc.api import Client
from solders.pubkey import Pubkey
from solders.keypair import Keypair
from solana.rpc.types import TxOpts
from solana.rpc.commitment import Confirmed , Finalized , Processed
from solders.account import Account
from solana import transaction
from solders.signature import Signature
import json
from .inf import env as ENV
import requests

new_client = Client("https://api.mainnet-beta.solana.com")

public_key = Pubkey.from_string(ENV.WALLET_ADDRESS)
def save_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)
def get_latest_block(publicKey:Pubkey):
    block_data = new_client.get_signatures_for_address(account=publicKey, before=None, until=None, limit=1,commitment=Finalized)
    return json.loads(block_data.to_json())['result'][0]

def get_tx(signature:Signature):
    data = new_client.get_transaction(signature,commitment=Finalized,max_supported_transaction_version=20).to_json()
    return json.loads(data)


def analyze_tx(transaction_data:dict):

    all_mints = transaction_data['result']['meta']['postTokenBalances']

    tokens = []
    data = [i['mint'] for i in all_mints if not i['mint']=='So11111111111111111111111111111111111111112']
    for j in data:
        if not j in tokens:
            tokens.append(j)

    return tokens








