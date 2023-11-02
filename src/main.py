import json
import os
import requests

from eth_account import Account

from config import BASE_URL, BROKER_ID
from register import add_access_key, register_account

account: Account = Account.from_key(os.environ.get("PRIVATE_KEY"))
print("Address:", account.address)

res = requests.get(
    "%s/v1/get_account?address=%s&broker_id=%s" % (BASE_URL, account.address, BROKER_ID)
)
response = json.loads(res.text)
print("get_account reponse:", response)

if response["success"]:
    account_id = response["data"]["account_id"]
else:
    account_id = register_account(account)

print("account_id:", account_id)

orderly_key = add_access_key(account)
print("orderly_key:", orderly_key)
