
# staking-deposit-grpc


*staking-deposit-grpc* is a GRPC wrapper for [staking-desposit-cli](https://github.com/ethereum/staking-deposit-cli)

[![Apache License 2.0](https://img.shields.io/github/license/neukind/staking-deposit-grpc)](https://github.com/peterblockman/staking-deposit-grpc/blob/main/LICENSE)
[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-v2.0%20adopted-ff69b4.svg)](CODE_OF_CONDUCT.md)

**Disclaimer: staking-deposit-grpc is still in beta. Use it at your own risk**
## Running staking-deposit-grpc

```bash
# clone the repository from Github

git clone git@github.com:neukind/staking-deposit-grpc.git

# create a Python virtual environment (venv)

python3 -m venv staking-deposit-grpc

cd staking-deposit-grpc

# activate the venv and install necessary Python dependencies

source bin/activate

pip install -r requirements.txt

# generate the Python libraries from protobuf definitions

./build_proto_libs.sh

# run the wallet service

./staking_deposit_service.py
```
## Usage 

See [service.proto](https://github.com/neukind/staking-deposit-grpc/blob/main/include/proto/service.proto)

## Tasks

 - :white_check_mark: Implement`new-mnemonic` 
 - :white_large_square: Implement `existing-mnemonic`  
 - :white_large_square: Increase test coverage
 - :white_large_square: CI

## Contributing

Contributions are always welcome in the form of [pull requests](https://github.com/neukind/staking-deposit-grpc/pulls). All contributions must follow the [community code of conduct](CODE_OF_CONDUCT.md).

To run the unit-test suite against your local Python installation, invoke `python -m unittest`.

## Contact

staking-deposit-grpc is brought to you by [Neukind](https://www.neukind.com/). Discussion is welcome on our [Discord server](https://discord.gg/x8TDzpPHcK).