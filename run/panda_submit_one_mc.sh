DS=$1
shift
SHORT_DS=$(echo $DS | sed -r 's/^.*mc.*7TeV\.([^\.]+\.[^\.]+)\..*$/\1/g')

prun                                                         \
    --inDS $DS \
    --outDS user.PeterWaller.purity.paumc.pass.$PASS.$SHORT_DS/  \
    --noBuild                                                                    \
    --outputs output.root                                                        \
    --nGBPerJob=3                                                              \
    --writeInputToTxt=IN:inputs.txt                                              \
    --exec './ana_run.sh --run-specific-output inputs.txt' \
    --tmpDir /tmp/pwaller/pass.$PASS/                                 \
    --athenaTag=16.0.2                                                           \
    $@ > /dev/null
