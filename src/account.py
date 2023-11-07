import base64
from datetime import datetime
import json
import math
import requests

from nacl.encoding import URLSafeBase64Encoder
from nacl.signing import SigningKey

from config import BASE_URL
from util import encode_key


def get_client_holding(orderly_account_id: str, orderly_key: SigningKey):
    d = datetime.utcnow()
    epoch = datetime(1970, 1, 1)
    timestamp = math.trunc((d - epoch).total_seconds() * 1_000)

    message = str(timestamp) + "GET" + "/v1/client/holding"
    print(message)
    orderly_signature = orderly_key.sign(
        message.encode(), encoder=URLSafeBase64Encoder
    ).decode("utf-8")
    print(orderly_signature)

    res = requests.get(
        "%s/v1/client/holding" % BASE_URL,
        headers={
            # "Content-Type": "application/x-www-form-urlencoded",
            "orderly-timestamp": str(timestamp),
            "orderly-account-id": orderly_account_id,
            "orderly-key": encode_key(orderly_key.verify_key._key),
            "orderly-signature": orderly_signature,
        },
        # params={
        #     "all": "false",
        # },
    )
    response = json.loads(res.text)
    print("get_client_holding:", response)
