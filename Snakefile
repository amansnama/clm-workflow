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

CASEROOT=f"{CASEDIR}/{CASENAME}"

# def 

rule all:
    input:
        f"{CASEROOT}/case.submit"

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
        ./clm_scripts/XMLCase.sh {CASEROOT} {XMLCONFIG}
        ./clm_scripts/Setup_Build_Case.sh {CASEROOT} --setup
        """

rule newcase:
    input:
        CONFIG
    output:
        CASEROOT + '/case.setup'
    shell:
        "./clm_scripts/CreateCase.sh {CASENAME} {CTSMDIR} {CASEDIR} {RES} {COMPSET}"