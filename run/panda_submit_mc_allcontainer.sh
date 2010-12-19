#! /usr/bin/env bash 

source /afs/cern.ch/atlas/offline/external/GRID/DA/panda-client/latest/etc/panda/panda_setup.sh

export PASS=23

prun                                                                      \
    --inDS user10.PeterWaller.pau.all_mc/                                 \
    --outDS user.PeterWaller.pau.all_mc.pass_$PASS/                       \
    --noBuild                                                             \
    --outputs output\*.root\*                                             \
    --nGBPerJob=3                                                         \
    --writeInputToTxt=IN:inputs.txt                                       \
    --exec './ana_run.sh --run-specific-output inputs.txt'                \
    --tmpDir /tmp/pwaller/pass.$PASS/                                     \
    --athenaTag=16.0.2                                                    \
    $@






