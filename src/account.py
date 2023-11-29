from datetime import datetime
from eth_account import Account as EthAccount
import json
from requests import Request, Session

from config import Config
from signer import Signer


class Account(object):
    def __init__(
        self,
        config: Config,
        session: Session,
        signer: Signer,
        account: EthAccount,
    ) -> None:
        self._config = config
        self._session = session
        self._signer = signer
        self._account = account

    def get_client_holding(self):
        req = self._signer.sign_request(
            Request("GET", "%s/v1/client/holding" % self._config.base_url)
        )
        res = self._session.send(req)
        response = json.loads(res.text)
        print("get_client_holding:", response)

        return response["data"]["holding"]
