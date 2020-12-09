# ctDNAtool

![Tests](https://github.com/Hogfeldt/ctDNAtool/workflows/Tests/badge.svg)

## setup
To install dependencies and install ctDNAtool it's recommended to first create a new clean Conda environment, an then run:
```
$ make init
```
This will install the dependencies as well as ctDNAtool. ctDNAtool will be installed in edit mode.

The software have two entrypoints `ctDNAtool`, which is have the core functinality, and `ctDNAflow` which defines a set of workflows, with what we consider the most commen use cases of the tool. 
To see which commands are available and how to use them, use the `--help` flag as shown below:
```
$ ctDNAflow --help
```

## Run tests
To let nox run the test suite, check for formatting and linting erros run:
```
$ make test
```
