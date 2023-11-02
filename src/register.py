from datetime import datetime
import json
import math
from base58 import b58encode
import requests

from eth_account import Account, messages
from web3 import Web3

from config import BASE_URL, BROKER_ID, CHAIN_ID
from eip712 import MESSAGE_TYPES, OFF_CHAIN_DOMAIN


def register_account(account: Account):
    res = requests.get("%s/v1/registration_nonce" % BASE_URL)
    response = json.loads(res.text)
    registration_nonce = response["data"]["registration_nonce"]

    d = datetime.utcnow()
    epoch = datetime(1970, 1, 1)
    timestamp = math.trunc((d - epoch).total_seconds() * 1_000)

    register_message = {
        "brokerId": BROKER_ID,
        "chainId": CHAIN_ID,
        "timestamp": timestamp,
        "registrationNonce": registration_nonce,
    }

    encoded_data = messages.encode_typed_data(
        domain_data=OFF_CHAIN_DOMAIN,
        message_types={"Registration": MESSAGE_TYPES["Registration"]},
        message_data=register_message,
    )
    signed_message = account.sign_message(encoded_data)

    res = requests.post(
        "%s/v1/register_account" % BASE_URL,
        headers={"Content-Type": "application/json"},
        json={
            "message": register_message,
            "signature": signed_message.signature.hex(),
            "userAddress": account.address,
        },
    )
    response = json.loads(res.text)
    print("register_account:", response)

    return response["data"]["account_id"]


def add_access_key(account: Account):
    w3 = Web3()
    key = w3.eth.account.create().key

    orderly_key = "ed25519:%s" % b58encode(key).decode("utf-8")

    d = datetime.utcnow()
    epoch = datetime(1970, 1, 1)
    timestamp = math.trunc((d - epoch).total_seconds() * 1_000)

    add_key_message = {
        "brokerId": BROKER_ID,
        "chainId": CHAIN_ID,
        "orderlyKey": orderly_key,
        "scope": "trading",
        "timestamp": timestamp,
        "expiration": timestamp + 1_000 * 60 * 60 * 24 * 365,  # 1 year
    }

    encoded_data = messages.encode_typed_data(
        domain_data=OFF_CHAIN_DOMAIN,
        message_types={"AddOrderlyKey": MESSAGE_TYPES["AddOrderlyKey"]},
        message_data=add_key_message,
    )
    signed_message = account.sign_message(encoded_data)

    res = requests.post(
        "%s/v1/orderly_key" % BASE_URL,
        headers={"Content-Type": "application/json"},
        json={
            "message": add_key_message,
            "signature": signed_message.signature.hex(),
            "userAddress": account.address,
        },
    )
    response = json.loads(res.text)
    print("register_account:", response)

    return response["data"]["orderly_key"]
