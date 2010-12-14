#! /usr/bin/env bash 

source /afs/cern.ch/atlas/offline/external/GRID/DA/panda-client/latest/etc/panda/panda_setup.sh

PASS=19

DS=mc09_7TeV.105814.JF70_pythia_jet_filter.merge.NTUP_PROMPTPHOT.e585_s765_s767_r1305_r1306_p231/
DSS=JF70
#DS=mc09_7TeV.105807.JF35_pythia_jet_filter.merge.NTUP_PROMPTPHOT.e505_s765_s767_r1305_r1306_p231/
#DSS=JF35

prun                                                         \
    --inDS $DS \
    --outDS user.PeterWaller.purity.paumc.pass.$PASS.$DSS/ \
    --noBuild                                                                    \
    --outputs output.root                                                        \
    --nFilesPerJob=1                                                              \
    --writeInputToTxt=IN:inputs.txt                                              \
    --exec './ana_run.sh inputs.txt' \
    --tmpDir /tmp/pwaller/pass.$PASS/                                 \
    --athenaTag=16.0.2                                                           \
    $@ 
