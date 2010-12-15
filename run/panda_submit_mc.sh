#! /usr/bin/env bash 

source /afs/cern.ch/atlas/offline/external/GRID/DA/panda-client/latest/etc/panda/panda_setup.sh

export PASS=21

cat all_mc_ds.txt | xargs -I{} -n1 -P10 ./panda_submit_one_mc.sh {} $@
