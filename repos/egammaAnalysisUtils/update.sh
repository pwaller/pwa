#! /usr/bin/env bash

set -u
set -e

SRC_REPO="${HOME}/afs/repos/egammaAnalysisUtils"
HEAD=$(cut -d/ -f3 ${SRC_REPO}/.git/HEAD)

if [ ! -e current_head ];
then
  echo empty > current_head;  
fi

if [[ "$(cat current_head)x" == "${HEAD}x" ]];
then
  echo "Already up to date!"
  exit 1;
fi

echo "Updating head"

cp -v ${SRC_REPO}/src/*.{cxx,C} egammaAnalysisUtils
cp -rv ${SRC_REPO}/egammaAnalysisUtils egammaAnalysisUtils/egammaAnalysisUtils 

# Don't import EnergyRescaler
rm egammaAnalysisUtils/EnergyRescaler*
rm egammaAnalysisUtils/egammaAnalysisUtils/EnergyRescaler*

echo "Success"
echo $HEAD > current_head
