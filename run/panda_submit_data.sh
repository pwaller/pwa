#! /usr/bin/env bash 

source /afs/cern.ch/atlas/offline/external/GRID/DA/panda-client/latest/etc/panda/panda_setup.sh

PASS=27

prun                                                                             \
    --inDS user.PeterWaller.PeriodDtoI.NTUP_PROMPTPHOT.p231/                   \
    --outDS user.PeterWaller.purity.pau.v15.pass_$PASS.good.period.A.to.I/       \
    --noBuild                                                                    \
    --outputs output\*.root\*                                                    \
    --nGBPerJob=MAX                                                                \
    --writeInputToTxt=IN:inputs.txt                                              \
    --exec './ana_run.sh --run-specific-output  -Gdata10_7TeV.pro05.merged_LBSUMM_eg_standard_7TeV.xml inputs.txt' \
    --tmpDir /tmp/pwaller/pass.$PASS/                                            \
    --athenaTag=16.0.2                                                           \
    $@ 
