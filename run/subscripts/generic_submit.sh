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
    --inDS $1                     \
    --outDS $2  \
    --extFile=./analysis.pybundle                                                 \
    --noBuild                                                                   \
    --outputs output\*.root\*                                \
    --nGBPerJob=4                                                               \
    --writeInputToTxt=IN:inputs.txt                                             \
    --exec "$3 inputs.txt" \
    --tmpDir /tmp/pwaller/pass.${PASS}.$4/                                         \
    --athenaTag=16.6.3 $5
