#! /usr/bin/env bash 

source /afs/cern.ch/atlas/offline/external/GRID/DA/panda-client/latest/etc/panda/panda_setup.sh

if ! ./prepare_submit.sh; then
  echo "Prepare submit failed."
  exit 1
fi;

PASS=$(cat bundle_tag)
EXTRA=$1

prun                                                                            \
    --inDS user.PeterWaller.data11_7TeV.Egamma_SMWZ.p503/                       \
    --outDS user.PeterWaller.data11_7TeV.Egamma_SMWZ.p503.gravcount.${PASS}/    \
    --noBuild                                                                   \
    --outputs output\*.root\*                                                   \
    --nGBPerJob=MAX                                                             \
    --writeInputToTxt=IN:inputs.txt                                             \
    --exec './ana_run.sh --run-specific-output -Ggrls/data11_7TeV.periodAllYear_DetStatus-v10-pro08-01_Eg_standard.xml inputs.txt' \
    --tmpDir /tmp/pwaller/pass.${PASS}/                                         \
    --athenaTag=16.6.3                                                          \
    $@ 
