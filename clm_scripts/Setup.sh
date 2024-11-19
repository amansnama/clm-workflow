#!/bin/bash -e

# Created on 2024/11/08 by Aman Shrestha
# Setup CLM

if [ "$#" -lt 2 ]; then
    echo "Usage: $0 <CASEROOT> --setup --build --xml"
    exit 1
fi

CASEROOT=$1     # Directory of current case

# Initialize flags to false
setup=false
build=false
xml=false

for arg in "${@:2}"; do
    case $arg in
        --setup) setup=true ;; # Flag to run setup
        --build) build=true ;; # Flag to run build
        --xml) xml=true ;; # Flag to change xmls
        *) 
            echo "Unexpected flag: $arg"
            exit 2 ;;
    esac
done 

# Output the values of the flags for debugging
echo "CASEROOT: $CASEROOT"
echo "Setup: $setup"
echo "Build: $build"
echo "XML: $xml"

SCRIPTDIR=$(pwd) # Dir with clm scripts

cd $CASEROOT

# Run case setup
if [ $setup = true ]; then
    ./case.setup
    echo "Case setup successfull!"
fi

# Find machine name
hostname_value=$(hostname)
# Run case build
if [ $build = true ]; then
    if [[ $hostname_value == "derecho"* ]]; then
        qcmd ./case.build
    else
        ./case.build
    fi
    echo "Case build successfull!"
fi

# Change XML
if [ $xml = true ]; then
    # Change directory back to clm-workflow/clm_scripts
    cd $SCRIPTDIR
    python run_xmlchange.py $CASEROOT xmlconfig.cfg
    echo "XML Changed!"
fi
