#! /usr/bin/env bash

set -u
set -e

source /afs/cern.ch/atlas/offline/external/GRID/DA/panda-client/latest/etc/panda/panda_setup.sh

if ! ./prepare_submit.sh; then
  echo "Prepare submit failed."
  exit 1
fi;

PASS=$(cat bundle_tag)

prun                                                                            \
    --inDS user.PeterWaller.skims.Xabier.D4.NTUP_PHOTON.f368_m806_p541.DR_Skim_v2/                       \
    --outDS user.PeterWaller.skims.Xabier.D4.NTUP_PHOTON.f368_m806_p541.DR_Skim_v2.gravcount.${PASS}/    \
    --extFile=./analysis.pybundle                                                 \
    --noBuild                                                                   \
    --outputs dumped_events.root,output\*.root\*                                \
    --nGBPerJob=4                                                             \
    --writeInputToTxt=IN:inputs.txt                                             \
    --exec './ana_run.sh --run-specific-output --release=rel16 --project=data11 -Ggrls/most_recent.xml inputs.txt' \
    --tmpDir /tmp/pwaller/pass.${PASS}/                                         \
    --athenaTag=16.6.3                                                          \
    --mergeOutput                                                               \
    $@ 
