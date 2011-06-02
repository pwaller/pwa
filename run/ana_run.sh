#! /usr/bin/env bash

./ana_bootstrap.py -v --distribute --never-download run_env
source run_env/bin/activate

python $(which pip) install analysis.pybundle

EXECUTABLE=$1
shift

python $(which $EXECUTABLE) $@
