#! /usr/bin/env bash 

source /afs/cern.ch/atlas/offline/external/GRID/DA/panda-client/latest/etc/panda/panda_setup.sh

if ! ./prepare_submit.sh; then
  echo "Prepare submit failed."
  exit 1
fi;

PASS=$(cat bundle_tag)
EXTRA=$1

prun                                                                             \
    --inDS user.PeterWaller.PeriodDtoI.NTUP_PROMPTPHOT.p404/                   \
    --outDS user.PeterWaller.purity.pau.v16.${PASS}${EXTRA}.good.period.D.to.I/       \
    --noBuild                                                                    \
    --outputs output\*.root\*                                                    \
    --nGBPerJob=MAX                                                                \
    --writeInputToTxt=IN:inputs.txt                                              \
    --exec './ana_run.sh --run-specific-output --v16 -Gdata10_7TeV.pro05.merged_LBSUMM_eg_standard_7TeV.xml inputs.txt' \
    --tmpDir /tmp/pwaller/pass.${PASS}/                                            \
    --athenaTag=16.0.2                                                           \
    $@ 
