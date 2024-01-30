#!/bin/bash

set -e

PYTHONPATH=$1

echo "PYTHONPATH = ${PYTHONPATH}"

echo "pwd = $(pwd)"
if [ ! -d "venv" ]; then
    ${PYTHONPATH} -m venv venv
    source venv/bin/activate
else
    echo "venv already exists"
fi
