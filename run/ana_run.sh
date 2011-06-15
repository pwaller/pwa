#! /usr/bin/env bash

# Peter Waller <peter.waller@cern.ch> circa 2011 Licensed under GPLv3.
# The purpose of this script is to bootstrap the analysis environment and run
# the software specified as arguments to it.

function timer()
{
    if [[ $# -eq 0 ]]; then
        echo $(date '+%s')
    else
        local  stime=$1
        etime=$(date '+%s')

        if [[ -z "$stime" ]]; then stime=$etime; fi

        dt=$((etime - stime))
        ds=$((dt % 60))
        dm=$(((dt / 60) % 60))
        dh=$((dt / 3600))
        printf '%d:%02d:%02d' $dh $dm $ds
    fi
}

START=$(timer)

echo "--- Starting. The time is:" $(date)

./ana_bootstrap.py -v --distribute --never-download run_env
source run_env/bin/activate

# Sometimes installed scripts don't have correct Shebang, so we run them with
# env's python with $(which X)
python $(which pip) install analysis.pybundle

EXECUTABLE=$1
shift

python $(which $EXECUTABLE) $@

echo "--- Finished. The time is:" $(date)
echo "--- Elapsed since start:" $(timer $START)
