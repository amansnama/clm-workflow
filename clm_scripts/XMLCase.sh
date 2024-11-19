#!/bin/bash -e

# Created on 2024/11/19 by Aman Shrestha

if [ "$#" -lt 2 ]; then
    echo "Usage: $0 <CASEROOT> <XMLCONFIG>"
    exit 1
fi

CASEROOT=$1     # Directory of current case
XMLCONFIG=$2    # Path to xmlconfig.cfg file

# Runs the python script run_xmlchange.py with two args
# realpath gets the absolute path of XMLCONFIG
python run_xmlchange.py $CASEROOT $(realpath "$XMLCONFIG")
exit 0