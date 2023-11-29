import json
import os
import requests

from eth_account import Account

from client import Client
from config import Config
from faucet import mint_test_usdc
from order import OrderType, Side


account: Account = Account.from_key(os.environ.get("PRIVATE_KEY"))
print("Address:", account.address)

config = Config()

client = Client(config, account)

symbols = client.public.get_symbols()
print("symbols:", symbols)

client.create_new_access_key()

holding = client.account.get_client_holding()

hasUSDC = any(
    list(
        map(
            lambda value: value["token"] == "USDC" and value["holding"] > 100.0, holding
        )
    )
)
if not hasUSDC:
    mint_test_usdc(config, account)

orders = client.order.get_orders()
print("get_orders:", orders)

res = client.order.create_order("PERP_ETH_USDC", OrderType.MARKET, 0.01, Side.BUY)
print("create_order:", res)

client.pnl.settle_pnl()
