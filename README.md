# `naas-wallet-service`

`naas-wallet-service` is a wallet generation service for NaaS.

## Running `naas-wallet-service`

```bash
# clone the repository from Github
git clone git@github.com:neukind/naas-wallet-service.git

# create a Python virtual environment (venv) in strawberryd/
python3 -m venv naas-wallet-service
cd naas-wallet-service

# initialize the Git submodules (for shared protobuf definitions)
git submodule update --init

# activate the venv and install necessary Python dependencies
source bin/activate
pip install -r requirements.txt

# generate the Python libraries from protobuf definitions
./build_proto_libs.sh

# run the wallet service
./wallet_service.py
```
