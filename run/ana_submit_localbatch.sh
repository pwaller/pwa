#! /usr/bin/env bash

export TAG=$(git describe --tags --exact-match --dirty 2> /dev/null)
export ARGUMENTS=$@

echo tag = $TAG
echo arguments = $ARGUMENTS

qsub -v ARGUMENTS,TAG \
	-q short64 -e /scratch/pwaller/output \
	-o /scratch/pwaller/output \
	ana_run_localbatch.sh
