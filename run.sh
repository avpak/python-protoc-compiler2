#!/bin/sh
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install protobuf
protoc --plugin=protoc-gen-custom=./plugin.py --custom_out=. xxx.proto

