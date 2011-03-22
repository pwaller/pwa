#! /usr/bin/env bash

source /afs/cern.ch/atlas/offline/external/GRID/ddm/DQ2Clients/setup.sh &> /dev/null

LAST_TAG=$(git describe --tags | cut -d'-' -f1)
LAST_N=$(echo $LAST_TAG | cut -d'.' -f2)

echo "Will fetch dataset for ${LAST_TAG} - ${LAST_N}"

dest_dir=/data1/pwaller/v15/passes/${LAST_N}
mkdir -p $dest_dir/mc
pushd $dest_dir
((dq2-get user.PeterWaller.purity.pau.v15.${LAST_TAG}.good.period.A.to.I/)
 2>&1 | mail -s "Done fetching Data v15.${LAST_TAG} (EOM)" pwaller) &
cd mc
((dq2-get user.PeterWaller.pau.v15.all_mc.pass_${LAST_TAG}./
user.PeterWaller.purity.pau.v15.${LAST_TAG}.good.period.A.to.I/)
 2>&1 | mail -s "Done fetching MC v15.${LAST_TAG} (EOM)" pwaller) &
popd

dest_dir=/data1/pwaller/v16/passes/${LAST_N}
mkdir -p $dest_dir
pushd $dest_dir
((dq2-get user.PeterWaller.purity.pau.v16.${LAST_TAG}.good.period.D.to.I/)
 2>&1 | mail -s "Done fetching v16.${LAST_TAG} (EOM)" pwaller) &
popd

echo "Fetching in the background."
