#! /usr/bin/env bash

export AtlasSetup=/batchsoft/atlas/athena/AtlasSetup
source $AtlasSetup/scripts/asetup.sh 16.6.3

ORIG_DIR=~/master/run
TMPDIR=$(mktemp -d)

pushd $TMPDIR
echo $TMPDIR

${ORIG_DIR}/ana_bootstrap.py -v --distribute run_env
source run_env/bin/activate

python $(which pip) install ${ORIG_DIR}/analysis.pybundle

python $(which pwa_graviton_counts) $ARGUMENTS

DEST=/scratch/pwaller/passes/${TAG}/$PBS_JOBID
mkdir -p $DEST
cp *.root* $DEST

popd
rm -R $TMPDIR
