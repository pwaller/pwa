#! /usr/bin/env bash 

source /afs/cern.ch/atlas/offline/external/GRID/DA/panda-client/latest/etc/panda/panda_setup.sh

if ! ./prepare_submit.sh; then
  echo "Prepare submit failed."
  exit 1
fi;

PASS=$(cat bundle_tag)
EXTRA=$1

prun                                                                            \
    --inDS user.PeterWaller.HSG1SKIM.NTUP_PHOTON.f371_m824_p541_v0003-v0004/    \
    --outDS user.PeterWaller.HSG1SKIM.NTUP_PHOTON.f371_m824_p541_v0003-v0004.gravcount.${PASS}/   \
    --extFile=./analysis.pybundle                                                 \
    --outputs dumped_events.root,output\*.root\*                                \
    --nGBPerJob=4                                                               \
    --writeInputToTxt=IN:inputs.txt                                             \
    --exec './ana_run.sh --run-specific-output --release=rel16 --project=data11 -Ggrls/most_recent.xml inputs.txt' \
    --tmpDir /tmp/pwaller/pass.${PASS}/                                         \
    --athenaTag=16.6.3                                                          \
    --mergeOutput                                                               \
    $@ 
