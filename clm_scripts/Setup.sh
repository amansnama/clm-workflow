#!/bin/bash -e

# Created on 2024/11/08 by Aman Shrestha
# Setup CLM

if [ "$#" -lt 1 ]; then
    echo "Usage: $0 <CASEROOT> [CONDAENV]"
    exit 1
fi

$CASEROOT=$1

cd $CASEROOT

# Run case setup
./case.setup

# Conda env
ml conda
conda activate $CONDAENV