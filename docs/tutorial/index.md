# Overview

The tutorial is seperated into three options based on which part(s) of the workflow the user will be running. The tutorial assumes the user will be running the workflow in a NCAR machine, specifically `derecho`. The advantages of running in a NCAR machine in comparison to a local machine are:

1. CLM simulations are computationally intensive and perform poorly in local machines or servers. NCAR hosts advanced supercomputing systems where they develop and test CLM.
2. Inputs required to run CLM simulations occupy huge space. A 40 year simulation could require ~500GB of atmospheric forcing data. The memory requirements also increase exponentially with finer resolution.

It is possible to run CLM in a non-NCAR machine; however, it requires major effort.

## Tutorial Prerequisite

### Installing CTSM

Installing CTSM (CTSM hosts CLM) is straightforward. Clone CTSM from their [github repo](https://github.com/ESCOMP/CTSM).
```
$ git clone https://github.com/ESCOMP/CTSM
```
By default, the clone command clones the latest commit from the master branch. The CTSM developers provide tags for incremental developments. To get a specific tag, say tag ctsm5.2.001, run:

```
$ git checkout ctsm5.2.001
```

`clm-workflow` needs to be informed where CTSM is installed. The path to CTSM is provided to the variable `CTSMDIR` in `caseconfig.cfg`. Throughout these tutorials, `CTSMDIR` should be the path where you installed CTSM.

CTSM is not fully installed yet. CTSM depends upon various dependencies which are linked to CTSM as git submodules. These can be installed by running
```
# For ctsm<5.2
$ cd CTSMDIR
$ ./manage_externals/checkout_externals

# For ctsm>5.2
$ cd CTSMDIR
$ ./bin/git-fleximod update
```

Please go through NCAR's [CTSM tutorial](https://github.com/NCAR/CTSM-Tutorial) for more information on runnning CTSM.

### Installing snakemake 

Follow the steps to install snakemake [here](https://snakemake.readthedocs.io/en/stable/getting_started/installation.html.) 

```
$ conda create -c conda-forge -c bioconda -n snakemake snakemake
```

## clm-workflow Installation

Clone the clm-workflow repo [https://github.com/amansnama/clm-workflow](https://github.com/amansnama/clm-workflow) to your machine.

```
$ git clone https://github.com/amansnama/clm-workflow
```

## Workflow Tutorials

- #### [CLM simulation workflow tutorial](clm-sim-tutorial.md)
- #### Analysis workflow tutorial
- #### Combined CLM-analysis workflow tutorial