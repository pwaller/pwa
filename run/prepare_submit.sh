#! /usr/bin/env bash

#if ! minty-runperiod-mapping -c; then
#    echo "Refusing to continue, period mapping out of date"
#    exit
#fi

CURRENT_TAG=$(git describe --tags --exact-match --dirty 2> /dev/null)
BUNDLE_TAG=$(cat bundle_tag)

if [[ "x${CURRENT_TAG}" == "x" ]]; then 
    echo "Getting the current tag failed"
    exit 1
fi

if [ $? -ne 0 ]; then
    echo "Working tree is not tagged!"
    exit 1
fi

if echo $CURRENT_TAG | grep dirty > /dev/null; then
    echo "Working tree is dirty!"
    exit 1
fi

echo Current tag is $CURRENT_TAG
echo Bundle tag is $BUNDLE_TAG

if [[ "$BUNDLE_TAG" != "$CURRENT_TAG" ]];
then
    echo "Rebuilding bundle.."
    pushd .. > /dev/null
    time ./bundle_build.sh > /dev/null
    popd > /dev/null
    echo $CURRENT_TAG > bundle_tag
fi

