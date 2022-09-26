
# `staking-deposit-grpc`


`staking-deposit-grpc` is a GRPC wrapper for [staking-desposit-cli](https://github.com/ethereum/staking-deposit-cli)


## Running `staking-deposit-grpc`

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

see [service.proto](https://github.com/neukind/staking-deposit-grpc/blob/main/include/proto/service.proto)

## Tasks

 - :white_check_mark: Implement`new-mnemonic` 
 - :white_large_square: Implement `existing-mnemonic`  
 - :white_large_square: Increase test coverage
