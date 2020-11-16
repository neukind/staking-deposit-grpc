#!/usr/bin/env python3

from eth2deposit import credentials, settings
from eth2deposit.utils import constants
from eth2deposit.key_handling import keystore
from eth2deposit.key_handling.key_derivation import mnemonic
import json


class WalletGenerator:
    mnemonic = ""
    password = ""
    idx = 0
    setting = {}

    def __init__(self, password, network):
        self.mnemonic = mnemonic.get_mnemonic(
            language="english",
            words_path="word_lists",
        )
        self.password = password
        self.setting = settings.get_setting(network)

    def generate_credential(self):
        cred = credentials.Credential(
            mnemonic=self.mnemonic,
            mnemonic_password="",
            index=self.idx,
            amount=32 * constants.ETH2GWEI,
            fork_version=self.setting.GENESIS_FORK_VERSION,
        )
        self.idx += 1

        deposit_data = json.dumps(cred.deposit_datum_dict, default=lambda x: x.hex())

        signing_keystore = cred.signing_keystore(self.password).as_json()
        ks_data = json.loads(signing_keystore)
        ks_crypto = keystore.KeystoreCrypto.from_json(ks_data["crypto"])
        ks = keystore.Keystore(
            crypto=ks_crypto,
            description=ks_data.get("description", ""),
            pubkey=ks_data.get("pubkey", ""),
            path=ks_data["path"],
            uuid=ks_data["uuid"],
            version=ks_data["version"],
        )
        ks_secret = ks.decrypt(self.password)
        if cred.signing_sk != int.from_bytes(ks_secret, "big"):
            return {}

        return {"deposit_data": deposit_data, "signing_keystore": signing_keystore}