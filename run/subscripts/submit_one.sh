#! /usr/bin/env bash

PASS=$(cat bundle_tag)

DS=$1
shift

prun                                                                            \
    --inDS $DS                                                                  \
    --outDS user.PeterWaller.mc10_7TeV.NTUP_SEVERAL.p503.gravcount.${PASS}/     \
    --noBuild                                                                   \
    --outputs output\*.root\*                                                   \
    --nGBPerJob=MAX                                                             \
    --writeInputToTxt=IN:inputs.txt                                             \
    --exec './ana_run.sh --run-specific-output  -Gdata11_7TeV.periodAllYear_DetStatus-v10-pro08-01_Eg_standard.xml inputs.txt' \
    --tmpDir /tmp/pwaller/pass.${PASS}/                                         \
    --athenaTag=16.6.3                                                          \
    $@ 
