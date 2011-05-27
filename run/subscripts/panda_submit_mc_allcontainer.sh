#! /usr/bin/env bash 

set -u
set -e

source /afs/cern.ch/atlas/offline/external/GRID/DA/panda-client/latest/etc/panda/panda_setup.sh

if ! ./prepare_submit.sh; then
  echo "Prepare submit failed."
  exit 1
fi;

PASS=$(cat bundle_tag)

prun                                                                      \
    --inDS user10.PeterWaller.pau.all_mc/                                 \
    --outDS user.PeterWaller.pau.all_mc.pass_$PASS/                       \
    --extFile=./analysis.pybundle                                                 \
    --noBuild                                                                   \
    --outputs dumped_events.root,output\*.root\*                                \
    --nGBPerJob=3                                                         \
    --writeInputToTxt=IN:inputs.txt                                       \
    --exec './ana_run.sh --run-specific-output inputs.txt'                \
    --tmpDir /tmp/pwaller/pass.$PASS/                                     \
    --athenaTag=16.0.2                                                    \
    $@






