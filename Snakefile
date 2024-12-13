# Read and parse the configuration file
def read_config(file_path):
    variables = {}
    with open(file_path, 'r') as f:
        for line in f:
            # Skip empty lines and comments
            line = line.strip().rstrip(",")
            if not line or line.startswith("#"):
                continue
            # Parse key-value pairs
            key, value = line.split("=", 1)
            variables[key.strip()] = value.strip().strip('"')
    return variables

# config file
CONFIG="clm_scripts/caseconfig.cfg"
var_dict=read_config(CONFIG)

CASENAME = var_dict.get("CASENAME")
CTSMDIR = var_dict.get("CTSMDIR")
CASEDIR = var_dict.get("CASEDIR")
RES = var_dict.get("RES")
COMPSET = var_dict.get("COMPSET")
XMLCONFIG = var_dict.get("XMLCONFIG")
ARCHIVE = var_dict.get("ARCHIVE")

CASEROOT=f"{CASEDIR}/{CASENAME}"
OUTROOT=f"{ARCHIVE}/{CASENAME}"

EMAIL = "shrest66@msu.edu"

rule all:
    input:
        OUTROOT
        
    onsuccess:
        shell("mail -s 'Snakemake DONE {CASENAME}' {EMAIL} < {log}")

    onerror:
        shell("mail -s 'Snakemake ERROR {CASENAME}' {EMAIL} < {log}")

rule case_run_submit:
    input:
        CASEROOT + '/case.submit'
    output:
        OUTROOT
    shell:
        """
        cd {CASEROOT}
        ./case.submit
        """

rule build:
    input:
        CASEROOT + '/case.build'
    output:
        CASEROOT + '/case.submit'
    shell:
        "./clm_scripts/Setup_Build_Case.sh {CASEROOT} --build"

rule setup:
    input:
        CASEROOT + '/case.setup'
    output:
        CASEROOT + '/case.build'
    shell:
        """
        cd clm_scripts
        ./XMLCase.sh {CASEROOT} {XMLCONFIG}
        ./Setup_Build_Case.sh {CASEROOT} --setup
        """

rule newcase:
    input:
        CONFIG
    output:
        CASEROOT + '/case.setup'
    shell:
        """
        if [ -d "{CASEROOT}" ]; then
            echo "Removing existing case directory {CASEROOT}"
            rm -rf "{CASEROOT}"
        fi
        ./clm_scripts/CreateCase.sh {CASENAME} {CTSMDIR} {CASEDIR} {RES} {COMPSET} $PRJ
        """