#!/usr/bin/env bash

cd $( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
source env/bin/activate
./records/query.py "$@"
