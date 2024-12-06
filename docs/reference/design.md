# clm-workflow Design

## Introduction

The goal of this workflow is to automate the bazillion steps of running CLM simulations in a highly reproducible manner. In addition, the secondary goal is to analyze the outputs of CLM simulations if CLM runs successfully. Finally, the workflow needs to provide a simulation report for successful and failed workflow runs.

## Design Considerations

1. CLM5 is developed, tested, and supported in NCAR machines. It is difficult but possible to run CLM5 in non-NCAR machines. A check for NCAR or non-NCAR machine will need to be included in the CLM simulation part of the workflow.
2. The analysis workflow consists of number of Python scripts and Jupyter notebooks. These depend on a set of libraries. So, a Python environment with a specific Python version and dependent libraries need to be installed.
3. Users should be provided the choice to run only CLM simulation, only output analysis, or both parts of the workflow.

### Constraints

- The snakemake workflow philosophy needs a 'master' job to be running in a batch job style system. For NCAR's derecho machine specifically, any job has a maximum allowable run time of 12 hours. So, even if a ./case.submit job of 12 hours starts instantly with the master job, there will not be adequate time to run the analysis part of the workflow. *A solution might be to split the master job into two master jobs: first for CLM simulation, and second for output analysis.*

## Algorithm or pseudocode of the main workflow components

```
{!pseudocode.txt!}
```