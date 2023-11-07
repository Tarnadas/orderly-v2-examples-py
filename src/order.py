import base64
from datetime import datetime
import json
import math
import requests

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from config import BASE_URL, BROKER_ID
from util import encode_key


def get_orders(orderly_account_id: str, orderly_key: Ed25519PrivateKey):
    d = datetime.utcnow()
    epoch = datetime(1970, 1, 1)
    timestamp = math.trunc((d - epoch).total_seconds() * 1_000)

    message = str(timestamp) + "GET" + "/v1/orders"
    orderly_signature = base64.urlsafe_b64encode(
        orderly_key.sign(message.encode())
    ).decode("utf-8")

    res = requests.get(
        "%s/v1/orders" % BASE_URL,
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "orderly-timestamp": str(timestamp),
            "orderly-account-id": orderly_account_id,
            "orderly-key": encode_key(orderly_key.public_key().public_bytes_raw()),
            "orderly-signature": orderly_signature,
        },
    )
    response = json.loads(res.text)
    # print("get_orders:", response)


def create_order(orderly_account_id: str, orderly_key: Ed25519PrivateKey):
    d = datetime.utcnow()
    epoch = datetime(1970, 1, 1)
    timestamp = math.trunc((d - epoch).total_seconds() * 1_000)

    data = {
        "symbol": "PERP_ETH_USDC",
        "order_type": "MARKET",
        "order_quantity": 0.01,
        "side": "BUY",
    }
    message = str(timestamp) + "POST" + "/v1/order" + json.dumps(data)
    print(message)
    orderly_signature = base64.urlsafe_b64encode(
        orderly_key.sign(message.encode())
    ).decode("utf-8")

    res = requests.post(
        "%s/v1/order" % BASE_URL,
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
    print("create_order:", response)
