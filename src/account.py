import base64
from datetime import datetime
import json
import math
import requests

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from config import BASE_URL
from util import encode_key


def get_client_holding(orderly_account_id: str, orderly_key: Ed25519PrivateKey):
    d = datetime.utcnow()
    epoch = datetime(1970, 1, 1)
    timestamp = math.trunc((d - epoch).total_seconds() * 1_000)

    message = str(timestamp) + "GET" + "/v1/client/holding"
    orderly_signature = base64.urlsafe_b64encode(
        orderly_key.sign(message.encode())
    ).decode("utf-8")

    res = requests.get(
        "%s/v1/client/holding" % BASE_URL,
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "orderly-timestamp": str(timestamp),
            "orderly-account-id": orderly_account_id,
            "orderly-key": encode_key(orderly_key.public_key().public_bytes_raw()),
            "orderly-signature": orderly_signature,
        },
    )
    response = json.loads(res.text)
    print("get_client_holding:", response)

    return response["data"]["holding"]
