# ctDNAtool

![Run tests](https://github.com/Hogfeldt/ctDNAtool/workflows/Run%20tests/badge.svg)
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>

## setup
To install dependencies and install ctDNAtool, it's recommended to first create a new clean Conda environment, and then run:
```
$ make init
```
This will install the dependencies as well as ctDNAtool. ctDNAtool will be installed in edit mode.

The software has two entrypoints: `ctDNAtool`, which contains the core functionality, and `ctDNAflow` which defines a set of workflows, with what we consider the most common use cases of the tool. 
To see which commands are available and how to use them, use the `--help` flag as shown below:
```
$ ctDNAflow --help
```

## Run tests
To let nox run the test suite, check for formatting and linting errors, run:
```
$ make test
```
