# Download input data for CLM simulation

CLM simulations require atmospheric forcing data, surface data, parameter data, and model domain meshes. These are available in NCAR's storage system 'GLADE'. CLM simulations in NCAR machine such as derecho or cheyenne are connected to the GLADE file system and therefore do not require users to download the input data.

## Non-NCAR machine

For users running CLM in a non-NCAR machine, input data are automatically downloaded before a CLM job can be submitted. 

To explicitly check for input data, run from your case directory.
```
$ ./check_input_data
```

To download missing input data,
```
$ ./check_input_data --download
```