import base64
from datetime import datetime
import json
import math

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from eth_account import Account, messages
import requests

from config import BASE_URL, BROKER_ID, CHAIN_ID
from eip712 import MESSAGE_TYPES, ON_CHAIN_DOMAIN
from util import encode_key


def settle_nonce(orderly_account_id: str, orderly_key: Ed25519PrivateKey) -> str:
    d = datetime.utcnow()
    epoch = datetime(1970, 1, 1)
    timestamp = math.trunc((d - epoch).total_seconds() * 1_000)

    message = str(timestamp) + "GET" + "/v1/settle_nonce"
    orderly_signature = base64.urlsafe_b64encode(
        orderly_key.sign(message.encode())
    ).decode("utf-8")

    res = requests.get(
        "%s/v1/settle_nonce" % BASE_URL,
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "orderly-timestamp": str(timestamp),
            "orderly-account-id": orderly_account_id,
            "orderly-key": encode_key(orderly_key.public_key().public_bytes_raw()),
            "orderly-signature": orderly_signature,
        },
    )
    response = json.loads(res.text)
    print("settle_nonce:", response)

    return response["data"]["settle_nonce"]


def settle_pnl(
    orderly_account_id: str,
    orderly_key: Ed25519PrivateKey,
    account: Account,
    nonce: str,
):
    d = datetime.utcnow()
    epoch = datetime(1970, 1, 1)
    timestamp = math.trunc((d - epoch).total_seconds() * 1_000)

    register_message = {
        "brokerId": BROKER_ID,
        "chainId": CHAIN_ID,
        "timestamp": timestamp,
        "settleNonce": nonce,
    }

    encoded_data = messages.encode_typed_data(
        domain_data=ON_CHAIN_DOMAIN,
        message_types={"SettlePnl": MESSAGE_TYPES["SettlePnl"]},
        message_data=register_message,
    )
    signed_message = account.sign_message(encoded_data)

    data = {
        "message": register_message,
        "signature": signed_message.signature.hex(),
        "userAddress": account.address,
        "verifyingContract": ON_CHAIN_DOMAIN["verifyingContract"],
    }
    message = str(timestamp) + "POST" + "/v1/settle_pnl" + json.dumps(data)
    orderly_signature = base64.urlsafe_b64encode(
        orderly_key.sign(message.encode())
    ).decode("utf-8")

    res = requests.post(
        "%s/v1/settle_pnl" % BASE_URL,
        headers={
            "Content-Type": "application/json",
            "orderly-timestamp": str(timestamp),
            "orderly-account-id": orderly_account_id,
            "orderly-key": encode_key(orderly_key.public_key().public_bytes_raw()),
            "orderly-signature": orderly_signature,
        },
        json=data,
    )
    response = json.loads(res.text)
    print("settle_pnl:", response)
