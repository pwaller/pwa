
LAST_TAG=$(git describe --tags | cut -d'-' -f1)
LAST_N=$(echo $LAST_TAG | cut -d'.' -f2)

echo "Processing release 15"

pushd /data1/pwaller/v15/passes/${LAST_N} &> /dev/null
    for P in {D..I}; do
        echo Processing period $P
        hmerge -f -Poutput-P${P} -operiod-${P}.root */*output*tgz* &> period${P}.log
    done
    hmerge -operiodD-I.root period*.root
popd

echo "Processing release 16"

pushd /data1/pwaller/v16/passes/${LAST_N} &> /dev/null
    for P in {D..I}; do
        echo Processing period $P  &> all.log
        hmerge -f -Poutput-P${P} -operiod-${P}.root */*output*tgz* &> period${P}.log
    done
    hmerge -operiodD-I.root period*.root
popd
