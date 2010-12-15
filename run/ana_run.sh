#! /usr/bin/env bash

./ana_bootstrap.py run_env
source run_env/bin/activate

python $(which pip) install analysis.pybundle

python $(which pwa_purity) $@
