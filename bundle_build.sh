#! /usr/bin/env bash

source env/bin/activate
if [ -e analysis.pybundle ]; then
    rm analysis.pybundle
fi 
pip bundle analysis.pybundle repos/{minty,pytuple,hmerge,OQMaps,PhotonIDTool,pwa,EnergyRescalerTool,commando}
rm -rf env/build-bundle*
