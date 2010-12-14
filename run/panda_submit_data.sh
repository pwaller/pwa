#! /usr/bin/env bash 

source /afs/cern.ch/atlas/offline/external/GRID/DA/panda-client/latest/etc/panda/panda_setup.sh

PASS=20

echo {B..I} |
tr ' ' $'\n' | 
xargs -I{} -n1 -P10 prun                                                         \
    --inDS group10.phys-sm.data10_7TeV.period{}.NoGRL.NTUP_PROMPTPHOT.p231/      \
    --outDS user.PeterWaller.purity.paudata.good.period.A.to.I.pass.$PASS.period{}/ \
    --noBuild                                                                    \
    --outputs output.root                                                        \
    --nGBPerJob=5                                                              \
    --writeInputToTxt=IN:inputs.txt                                              \
    --exec './ana_run.sh inputs.txt' \
    --tmpDir /tmp/pwaller/pass.$PASS.period{}/                                 \
    --athenaTag=16.0.2                                                           \
    $@ 
