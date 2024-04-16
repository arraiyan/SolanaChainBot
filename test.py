from solana.rpc.api import Client
from solders.pubkey import Pubkey
from solders.keypair import Keypair
from solana.rpc.types import TxOpts
from solana.rpc.commitment import Confirmed ,Finalized , Single , Processed , Commitment 
from solders.account import Account
from solana import transaction
from solders.signature import Signature
import json
import time


new_client = Client("https://api.mainnet-beta.solana.com")

public_key = Pubkey.from_string('DCA265Vj8a9CEuX1eb1LWRnDT7uK6q1xMipnNyatn23M')
balance = new_client.get_balance(pubkey=public_key)

get_latest_block = new_client.get_signatures_for_address(account=public_key, before=None, until=None, limit=1,commitment=Finalized)



result = json.loads(get_latest_block.to_json())['result'][0]


print(result)

import requests
def save_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)
def get_latest_transactions(block_number):
    # Solana RPC endpoint
    rpc_endpoint = 'https://api.mainnet-beta.solana.com'

    # Construct the RPC request payload
    payload =     {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "getTransaction",
    "params": [
      "3Xs7oJi3ePU8EstwzY5xR9MxBR4ZHJNytxpPuJ4ddaYZtB85921Z4J1bA9Cq2VC19Ce7ujomAFiwfTQcf11GsBHy",
      "json"

    ],
    "maxSupportedTransactionVersion":1,
  }
   
    response = requests.post(rpc_endpoint, json=payload)
    print(response)
    data = response.json()
    save_json(data, 'data.json')

# get_latest_transactions(258335132)
json_data = new_client.get_transaction(Signature.from_string('63yhAoP7KM2HRDQ8UPf9FGhhJGPUYwd8RZAK8wQSRaQtyWSzdA3QzMPiguvFY6v7STjhbLRauCrpi8Y1HSLNbhfL'),commitment=Finalized,max_supported_transaction_version=20).to_json()
save_json(json.loads(json_data),'data.json')





