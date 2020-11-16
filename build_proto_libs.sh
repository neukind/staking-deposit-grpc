#!/bin/bash
set -e
cd "$(dirname "$0")"

# create directory to store compiled output
mkdir -p proto

# build necessary Python libraries for gRPC from protobuf definitions
python -m grpc_tools.protoc \
    -Iinclude/naas-proto \
    --python_out=proto \
    --grpc_python_out=proto \
    include/naas-proto/wallet/service.proto
