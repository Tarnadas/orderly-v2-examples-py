import json
from base58 import b58encode
from eth_account import Account
import requests
from web3 import Web3

from config import BROKER_ID, CHAIN_ID


def mint_test_usdc(account: Account):
    res = requests.post(
        "https://testnet-operator-evm.orderly.org/v1/faucet/usdc",
        headers={"Content-Type": "application/json"},
        json={
            "broker_id": BROKER_ID,
            "chain_id": str(CHAIN_ID),
            "user_address": account.address,
        },
    )
    print(res.text)
    response = json.loads(res.text)
    print("mint_test_usdc:", response)
