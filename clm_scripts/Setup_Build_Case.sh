#!/bin/bash -e

# Created on 2024/11/08 by Aman Shrestha
# Script to setup and build case

if [ "$#" -lt 2 ]; then
    echo "Usage: $0 <CASEROOT> --setup --build"
    exit 1
fi

CASEROOT=$1     # Directory of current case

# Initialize flags to false
setup=false
build=false

for arg in "${@:2}"; do
    case $arg in
        --setup) setup=true ;; # Flag to run setup
        --build) build=true ;; # Flag to run build
        *) 
            echo "Unexpected flag: $arg"
            exit 2 ;;
    esac
done 

# Output the values of the flags for debugging
echo "CASEROOT: $CASEROOT"
echo "Setup: $setup"
echo "Build: $build"

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
        echo "Building in" $hostname_value
        qcmd -A $PRJ ./case.build
        # PRJ is an environmental variable
    else
        ./case.build
    fi
    echo "Case build successfull!"
fi

exit 0