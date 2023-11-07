import json
import os
import requests

from eth_account import Account

from account import get_client_holding
from config import BASE_URL, BROKER_ID
from faucet import mint_test_usdc
from order import create_order, get_orders
from pnl import settle_nonce, settle_pnl
from register import add_access_key, register_account

account: Account = Account.from_key(os.environ.get("PRIVATE_KEY"))
print("Address:", account.address)

res = requests.get(
    "%s/v1/get_account?address=%s&broker_id=%s" % (BASE_URL, account.address, BROKER_ID)
)
response = json.loads(res.text)
print("get_account reponse:", response)

if response["success"]:
    orderly_account_id: str = response["data"]["account_id"]
else:
    orderly_account_id = register_account(account)

print("account_id:", orderly_account_id)

orderly_key = add_access_key(account)

holding = get_client_holding(orderly_account_id, orderly_key)

hasUSDC = any(
    list(
        map(
            lambda value: value["token"] == "USDC" and value["holding"] > 100.0, holding
        )
    )
)
if not hasUSDC:
    mint_test_usdc(account)

res = requests.get("%s/v1/public/info" % BASE_URL)
response = json.loads(res.text)
symbols = response["data"]["rows"]

get_orders(orderly_account_id, orderly_key)

create_order(orderly_account_id, orderly_key)

nonce = settle_nonce(orderly_account_id, orderly_key)
settle_pnl(orderly_account_id, orderly_key, account, nonce)
