# Snakefile for automating the setup, build, and execution of CTSM cases

# Read and parse the configuration file
def read_config(file_path):
    """
    Reads config file and returns a dictionary of variables.

    Args:
        file_path (str): Path to the config file.
    
    Returns:
        dict: Dictionary of config variables.
    """
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

# Define config file and parse it
CONFIG="clm_scripts/caseconfig.cfg"
var_dict=read_config(CONFIG)

# Extract variables from the configuration dictionary
CASENAME = var_dict.get("CASENAME")
CTSMDIR = var_dict.get("CTSMDIR")
CASEDIR = var_dict.get("CASEDIR")
RES = var_dict.get("RES")
COMPSET = var_dict.get("COMPSET")
XMLCONFIG = var_dict.get("XMLCONFIG")
ARCHIVE = var_dict.get("ARCHIVE")

# Paths for case root and output directory
CASEROOT=f"{CASEDIR}/{CASENAME}"
OUTROOT=f"{ARCHIVE}/{CASENAME}"

# Email address for notifications
EMAIL = "shrest66@msu.edu"

# Overall workflow rule
rule all:
    input:
        OUTROOT # Final output directory
        
    # Notify success and error via email
    onsuccess:
        shell("mail -s 'Snakemake DONE {CASENAME}' {EMAIL} < {log}")

    onerror:
        shell("mail -s 'Snakemake ERROR {CASENAME}' {EMAIL} < {log}")

# Rule to run and submit the CLM case
rule case_run_submit:
    input:
        CASEROOT + '/case.submit'
    output:
        OUTROOT
    shell:
        # Submits the case to the machine's batch job system
        """
        cd {CASEROOT}
        ./case.submit
        """

# Rule to build the CLM case
rule build:
    input:
        CASEROOT + '/case.build'
    output:
        CASEROOT + '/case.submit'
    shell:
        # Builds the case
        "./clm_scripts/Setup_Build_Case.sh {CASEROOT} --build"

# Rule to set up the CLM case
rule setup:
    input:
        CASEROOT + '/case.setup'
    output:
        CASEROOT + '/case.build'
    shell:
        # Apply xml configurations to the case
        # Then setups the case
        """
        cd clm_scripts
        ./XMLCase.sh {CASEROOT} {XMLCONFIG}
        ./Setup_Build_Case.sh {CASEROOT} --setup
        """

# Rule to create a new CLM case
rule newcase:
    input:
        CONFIG # Input configuration file
    output:
        CASEROOT + '/case.setup'
    shell:
        # Creates newcase.
        # Forcefully removes case dir if it already exists
        """
        if [ -d "{CASEROOT}" ]; then
            echo "Removing existing case directory {CASEROOT}"
            rm -rf "{CASEROOT}"
        fi
        ./clm_scripts/CreateCase.sh {CASENAME} {CTSMDIR} {CASEDIR} {RES} {COMPSET} $PRJ
        """