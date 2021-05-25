#!/usr/bin/env python3

from eth2deposit import credentials, settings
from eth2deposit.key_handling import keystore
from eth2deposit.key_handling.key_derivation import mnemonic
import json


class WalletGenerator:
    """
    Class that generates an ETH2.0 wallet and validator keys.

    When the class is instantiated, a wallet mnemonic is created. After this,
    you can call `generate_credential` to make a new validator key inside the
    wallet.
    """

    mnemonic = ""
    password = ""
    idx = 0
    setting = {}
    amount = 0

    def __init__(self, password, network, amount):
        self.mnemonic = mnemonic.get_mnemonic(
            language="english",
            words_path="word_lists",
        )
        print(self.mnemonic)
        self.password = password
        self.setting = settings.get_chain_setting(network)
        self.amount = amount

    def generate_credential(self):
        """
        Generate a single ETH2.0 validator keypair.
        """

        cred = credentials.Credential(
            mnemonic=self.mnemonic,
            mnemonic_password="",
            index=self.idx,
            amount=self.amount,
            chain_setting=self.setting,
            hex_eth1_withdrawal_address=None
        )

        # Increment the index so we generate a new key next time.
        self.idx += 1

        # Create the deposit data JSON.
        deposit_data = json.dumps(cred.deposit_datum_dict, default=lambda x: x.hex())

        # Export the validator keystore.
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

        # Verify that the keystore decrypts correctly.
        ks_secret = ks.decrypt(self.password)
        if cred.signing_sk != int.from_bytes(ks_secret, "big"):
            return {}

        return {"deposit_data": deposit_data, "signing_keystore": signing_keystore}