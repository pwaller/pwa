#! /usr/bin/env bash

# Heuristic: Get the largest GRL. It's probably the most recent.

P=/afs/cern.ch/user/a/atlasdqm/www/grlgen/CombinedPerf/Egamma/Eg_standard_v5

cp $(ls -1S ${P}/data11* | head -n1) .
