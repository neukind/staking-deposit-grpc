import unittest
import warnings
import os
import json

from keys_generator import KeysGenerator
from staking_deposit import settings
from staking_deposit.key_handling.key_derivation import mnemonic
from eth_utils import decode_hex
from staking_deposit.utils.constants import ETH1_ADDRESS_WITHDRAWAL_PREFIX


class KeysGeneratorTest(unittest.TestCase):
    def setUp(self):
        warnings.simplefilter("ignore", ResourceWarning)
        self.keystore_password = "securepw"
        self.settings = settings
        self.amount = 32000000000
        self.chains_settings = [
            settings.MAINNET,
            settings.ROPSTEN,
            settings.GOERLI,
            settings.PRATER,
            settings.KILN,
            settings.SEPOLIA,
        ]

    def gen_mnemonic(self, chain_setting):
        gen = KeysGenerator(self.keystore_password, chain_setting, self.amount)
        gen_mnemonic = gen.mnemonic
        WORD_LISTS_PATH = os.path.join(
            os.getcwd(),
            "src",
            "staking-deposit",
            "staking_deposit",
            "key_handling",
            "key_derivation",
            "word_lists",
        )
        recon_mnemonic = mnemonic.reconstruct_mnemonic(
            gen_mnemonic, words_path=WORD_LISTS_PATH
        )
        self.assertEqual(gen_mnemonic, recon_mnemonic)
        return {gen_mnemonic, recon_mnemonic}

    def test_mnemonic_chains(self):
        for chain_settings in self.chains_settings:
            self.gen_mnemonic(chain_settings)

    def generate_credential(self, chain_settings):
        gen = KeysGenerator(self.keystore_password, chain_settings, self.amount)
        cred = gen.generate_credential()
        self.assertTrue("deposit_data" in cred)
        self.assertTrue("signing_keystore" in cred)

        deposit_data = json.loads(cred["deposit_data"])
        # Prater is Goerli's old name
        if chain_settings != settings.PRATER:
            self.assertEqual(
                deposit_data["network_name"],
                chain_settings,
            )
        elif chain_settings == settings.PRATER:
            self.assertEqual(deposit_data["network_name"], settings.GOERLI)
        else:
            self.fail(self, "test_generate_credential")

    def test_generate_credential(self):
        for chain_settings in self.chains_settings:
            self.generate_credential(chain_settings)

    def test_generate_credential_eth1_withdrawal_address(self):
        eth1_withdrawal_address = "0x1cae67c3889a07A6ED0Bb4295446E131A8A5f2C9"
        gen = KeysGenerator(
            self.keystore_password,
            self.settings.MAINNET,
            self.amount,
            "english",
            eth1_withdrawal_address,
        )
        cred = gen.generate_credential()
        self.assertTrue("deposit_data" in cred)
        self.assertTrue("signing_keystore" in cred)

        withdrawal_credentials = bytes.fromhex(
            json.loads(cred["deposit_data"])["withdrawal_credentials"]
        )
        assert withdrawal_credentials == (
            ETH1_ADDRESS_WITHDRAWAL_PREFIX
            + b"\x00" * 11
            + decode_hex(eth1_withdrawal_address)
        )


if __name__ == "__main__":
    unittest.main()
