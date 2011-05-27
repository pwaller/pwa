#! /usr/bin/env bash 

set -u
set -e

source /afs/cern.ch/atlas/offline/external/GRID/DA/panda-client/latest/etc/panda/panda_setup.sh

if ! ./prepare_submit.sh; then
  echo "Prepare submit failed."
  exit 1
fi;

PASS=$(cat bundle_tag)
EXTRA=$1

prun                                                                             \
    --inDS user.PeterWaller.PeriodDtoI.NTUP_PROMPTPHOT.p231/                   \
    --outDS user.PeterWaller.purity.pau.v15.${PASS}${EXTRA}.good.period.D.to.I/       \
    --extFile=./analysis.pybundle                                                 \
    --noBuild                                                                   \
    --outputs dumped_events.root,output\*.root\*                                \
    --nGBPerJob=4                                                                \
    --writeInputToTxt=IN:inputs.txt                                              \
    --exec './ana_run.sh --run-specific-output --release=rel15 --project=data10 -Ggrls/data10_7TeV.pro04.merged_LBSUMM_eg_standard_7TeV.xml inputs.txt' \
    --tmpDir /tmp/pwaller/pass.${PASS}/                                            \
    --athenaTag=16.0.2                                                           \
    --mergeOutput                                                               \
    $@ 
