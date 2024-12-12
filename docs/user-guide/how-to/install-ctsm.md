# Installing CTSM

1. Clone the CTSM repo to your system.
    `$ git clone https://github.com/ESCOMP/CTSM`
2. The git clone command by default clones the most recent commit of the master/main branch. To clone a specific commit, use `$ git checkout`.
3. Checkout CTSM dependencies. This can be done by running a CTSM command `./manage_externals/checkout_externals/` for ctsm<5.2 or `./bin/git-fleximod update` for ctsm>5.2.