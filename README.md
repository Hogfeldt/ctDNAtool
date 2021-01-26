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
or
```
$ ctDNAtool --help
```

## Testing
To run the test suite with nox, check for formatting and linting errors, run:
```
$ make test
```

To run just the linter, run:
```
$ make lint
```

## Debugging
To debug an invocation of the ctDNAtool, use the -d flag after ctDNAtool, as shown below.
```
$ ctDNAtool -d <COMMAND>
```

# ctDNAflow
ctDNAflow is a tool for running workflows, based on the commands found in ctDNAtool.
The workflows are compositions of multiple commands from ctDNAtool, and are designed with usability in mind.

Usage:

``` console
$ ctDNAflow length-data-bed-bin <reference_genome_path> <BAM_file_path>

$ ctDNAflow length-data-chr-bin <reference_genome_path> <BAM_file_path>
```

## Examples
The following is an example of an invocation of the command length-data-chr-bin. The command generates length data from
a BAM file and bins it in chromosomes, then writes the output to a .tsv file.

```
$ ctDNAflow length-data-chr-bin hg19.2bit sample.bam -o length_data.tsv
```

In the example above, the output is directed to the length_data.tsv file. 


Further documentation can be found by passing --help after ctDNAflow, or after a
specific command.

## Output
The output of the commands are written to either a .pickle or .tsv file. For the commands concerning only length data, the default
action is to write the output to a .tsv file. The output can be written to a .picke file by passing the -p flag.
For all other commands, the output is written to .pickle.
The output can be directed using the -o option. If this is not provided, the output will be written to a default filename.
