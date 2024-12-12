# CLM simulation workflow tutorial

This tutorial walks through the workflow to automate CLM simulations. Please ensure that CTSM is installed. The path where we installed CTSM is called `CTSMDIR`, throughout the tutorial and by `clm-workflow`.

1. CLM simulations are called cases. The manual way to create and run a CLM case would be to:
    - Create new case.
    - Run case setup.
    - Configure the settings that the CLM case will run on.
    - Build the case.
    - Submit the case run to a batch job queue.
2. `clm-workflow` automates all of the above steps. We instruct the workflow how we want the CLM case to be created, configured, and ran. These settings are specified in two files: `caseconfig.cfg` and `xmlconfig.cfg` inside the directory clm_scripts.
3. First, we will look inside `caseconfig.cfg`. It contains the variables `CASENAME, CTSMDIR, CASEDIR, RES, COMPSET, XMLCONFIG, and ARCHIVE`.
    - `CASENAME`: Name to identify the case. Can be anything.
    - `CTSMDIR`: Location of CTSM installation.
    - `CASEDIR`: Location to save new cases.
    - `RES`: CLM simulation spatial resolution. Valid RES values can be queried by running `CTSMDIR/cime/scripts/query_config --res`.
    - `COMPSET`: CLM component sets. Valid COMPSET can be queried by running `CTSMDIR/cime/scripts/query_config --compsets clm`.
    - `XMLCONFIG`: Location of xmlconfig.cfg file. The xmlconfig.cfg contains CLM xml build and run configurations.
    - `ARCHIVE`: Location to save CLM simulation outputs. The outputs may require a large storage space.
    ```
    CASENAME="name_to_identify_case",
    CTSMDIR="path_to_ctsm",
    CASEDIR="path_to_store_CASENAME",
    RES="CLM_grid_resolution",
    COMPSET="CLM_compset",
    XMLCONFIG="path_to_xmlconfig.cfg",
    ARCHIVE="path_to_CTSM_archive"
    ```

4. Derecho requires a mandatory project account to bill compute hour uses. Other machines might also require a project account. So, create an environment variable `PRJ` and store your project account in it. We will create `PRJ` in a `.profile` file in your home directory.
    ```
    $ cd ~
    $ echo 'PRJ=YOUR_PROJECT_ACCOUNT;export PRJ'>>.profile
    ```
    This will add `PRJ` to an environment variable after a new login. To make it available in the current login, run:
    ```
    $ source ~/.profile
    ```

5. `xmlconfig.cfg` contains xml configurations which define a CLM run. All possible xmls can be viewed by running `./xmlquery --listall`. It is best to always have xmlconfigs for `RUN_STARTDATE, STOP_N, and STOP_OPTION`. For this tutorial, we will run CLM for 5 days starting 2000-01-01 and let the maximume job wallclock of 30 minutes.
```
RUN_STARTDATE=2000-01-01
STOP_N=5
STOP_OPTION=ndays
JOB_WALLCLOCK_TIME=00:30:00
```

6. Activate our snakemake environment. First, we will load conda module. Then activate our snakemake environment `snakemake_env`.
```
$ ml conda
$ conda activate snakemake_env
```

7. We are all set up to run the workflow! Just type `snakemake` to run the workflow.
```
$ snakemake
```