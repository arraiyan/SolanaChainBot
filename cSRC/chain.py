from dexteritysdk.dex.sdk_context import SDKContext, SDKTrader
from solana.rpc.async_api import AsyncClient 
from solana.rpc.api import Client
from solders.keypair import Keypair
from solders.pubkey import Pubkey
import requests


solana_client = Client('https://solana-mainnet.g.alchemy.com/v2/uhJMLwtnUi_yGWgsvX5GNqSJk2-fh9WW')
def market_data(token_address):
    cg_api_url = f"https://api.coingecko.com/api/v3/coins/solana/contract/{token_address}"
    response = requests.get(cg_api_url)
    market_cap = "N/A"
    buy_requests = "N/A"
    exchange_rate = "N/A"
    if response.status_code == 200:
        data = response.json()
        if "market_data" in data:
            market_cap = data['market_data']["market_cap"]["usd"]
        if "market_cap_rank" in data:
            market_rank = data["market_cap_rank"]
        if "market_data" in data and "current_price" in data["market_data"] and "usd" in data["market_data"]["current_price"]:
            exchange_rate = float(data["market_data"]["current_price"]["usd"]) 

        name = data['name']
        liquidity = data.get("liquidity",None)
        print(data)
        return market_cap , market_rank , exchange_rate , name 



def get_liqui(token_address):
    market_address = ''
    order_book = solana_client.get_orderbook(market_address)
    liquidity = calculate_liquidity(order_book)
    return liquidity

def calculate_liquidity(order_book: dict) -> int:
    total_bid_size = sum(bid['size'] for bid in order_book['bids'])
    total_ask_size = sum(ask['size'] for ask in order_book['asks'])
    liquidity = min(total_bid_size, total_ask_size)
    return liquidity


