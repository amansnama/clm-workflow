#!/bin/bash -ue

# Created on 2024/11/08 by Aman Shrestha
# Creates new CLM case
# PROJECT needed for derecho, not for HPCC

# Checks for atleast 5 arguments
if [ "$#" -lt 5 ]; then
    echo "Usage: $0 <CASENAME> <CTSMDIR> <CASEDIR> <RES> <COMPSET> [PROJECT]"
    exit 1
fi

# Assign command-line arguments to variables
CASENAME="$1"       # Case name. Give any name you want
CTSMDIR="$2"        # Path to the ctsm directory
CASEDIR="$3"        # Directory where cases will be created
RES="$4"            # Resolution. Check ./query_config --grids
COMPSET="$5"        # Compset. Check ./query_config --compsets

cd ${CTSMDIR}/cime/scripts

if [ -n "${6-}" ]; then
    PROJECT="$6"        # Project to bill core-hours.
    ./create_newcase --case ${CASEDIR}/${CASENAME} --compset ${COMPSET} --res ${RES} --project ${PROJECT} --run-unsupported
else
    echo "PROJECT not provided. Running create_newcase without --project."
    ./create_newcase --case ${CASEDIR}/${CASENAME} --compset ${COMPSET} --res ${RES} --run-unsupported
fi
exit 0