#!/usr/bin/env python3

import os
import sys

# add proto/ to include path to fix import error
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "proto")))

from concurrent import futures
from eth2deposit import settings
from proto.wallet import service_pb2, service_pb2_grpc
from wallet_generator import WalletGenerator
import logging
import grpc


class WalletService(service_pb2_grpc.WalletServiceServicer):
    """
    RPC handler for the wallet service.

    Currently has one handler, which generates an ETH2.0 wallet.
    """

    def MakeWallet(self, request, context):
        """
        Make an ETH2.0 wallet.
        """
        response = service_pb2.MakeWalletResponse()

        gen = WalletGenerator(request.password, self._GetNetwork(request.network))

        # Generate the appropriate number of validator keys.
        for _ in range(0, request.numKeysToGenerate):
            cred_proto = response.credentials.add()
            cred = gen.generate_credential()
            if cred == {}:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("Failed to verify a signing keystore")
                return service_pb2.MakeWalletResponse()
            cred_proto.deposit_data = cred["deposit_data"]
            cred_proto.signing_keystore = cred["signing_keystore"]

        response.mnemonic = gen.mnemonic
        return response

    @staticmethod
    def _GetNetwork(network_enum):
        """
        Convert an ETH network (mainnet, testnet) from the protobuf enum to the
        enum used by the `eth2deposit` library.
        """
        if network_enum == service_pb2.MakeWalletRequest.EthNetwork.MAINNET:
            return settings.MAINNET
        elif network_enum == service_pb2.MakeWalletRequest.EthNetwork.TESTNET_MEDALLA:
            return settings.MEDALLA
        else:
            return ""


if __name__ == "__main__":
    logging.basicConfig()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    service_pb2_grpc.add_WalletServiceServicer_to_server(WalletService(), server)
    server.add_insecure_port(os.getenv("GRPC_BIND_URI", "[::]:50051"))
    server.start()
    server.wait_for_termination()
