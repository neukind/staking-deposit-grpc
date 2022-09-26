#!/usr/bin/env python3

import os
import sys

# add proto/ to include path to fix import error
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "proto")))

from concurrent import futures
from staking_deposit import settings
from staking_deposit.utils import constants
from proto import service_pb2, service_pb2_grpc
from keys_generator import KeysGenerator
from constants import mnemonic_languages
import logging
import grpc


class StakingDepositService(service_pb2_grpc.StakingDepositServiceServicer):
    """
    RPC handler for the staking deposit service.

    Currently has one handler, which generates a new mnemonic
    """

    def NewMnemonic(self, request, context):
        """
        Make an ETH2.0 wallet.
        """

        response = service_pb2.NewMnemonicResponse()
        amount = 32 * constants.ETH2GWEI
        if request.amount != 0:
            amount = request.amount
        gen = KeysGenerator(
            request.keystore_password,
            self._GetChain(request.chain),
            amount,
            self._GetMnemonicLanguage(request.mnemonic_language),
        )

        # Generate the appropriate number of validator keys.
        for _ in range(0, request.num_validators):
            cred_proto = response.credentials.add()
            cred = gen.generate_credential()
            if cred == {}:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("Failed to verify a signing keystore")
                return service_pb2.NewMnemonicResponse()
            cred_proto.deposit_data = cred["deposit_data"]
            cred_proto.signing_keystore = cred["signing_keystore"]

        response.mnemonic = gen.mnemonic
        return response

    @staticmethod
    def _GetChain(network_enum):
        """
        Convert an ETH chain (mainnet, testnet) from the protobuf enum to the
        enum used by the `staking_deposit` library.
        """
        if network_enum == service_pb2.Chain.MAINNET:
            return settings.MAINNET
        elif network_enum == service_pb2.Chain.ROPSTEN:
            return settings.ROPSTEN
        elif network_enum == service_pb2.Chain.GOERLI:
            return settings.GOERLI
        elif network_enum == service_pb2.Chain.PRATER:
            return settings.PRATER
        elif network_enum == service_pb2.Chain.KILN:
            return settings.KILN
        elif network_enum == service_pb2.Chain.SEPOLIA:
            return settings.SEPOLIA
        else:
            return ""

    @staticmethod
    def _GetMnemonicLanguage(mnemonic_language_enum):
        """
        Convert an mnemonic language from the protobuf enum to the
        language strings used by the `staking_deposit` library.
        """
        mnemonic_language = mnemonic_languages[mnemonic_language_enum]
        return mnemonic_language


if __name__ == "__main__":
    logging.basicConfig()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    service_pb2_grpc.add_StakingDepositServiceServicer_to_server(
        StakingDepositService(), server
    )

    bind_uri = os.getenv("GRPC_BIND_URI", "[::]:50051")
    server.add_insecure_port(bind_uri)
    server.start()
    print("Server started on %s" % bind_uri)
    server.wait_for_termination()
