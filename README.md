# memory_map_manager
Manages memory map generation in C, python and documentation written in python3.

# Installation

## Install from pip
Stable versions can be installed with:
```
pip install memory-map-manager
```

## Install from source
To install or update from sources checkout the repo and run:
```
python setup.py install --user -f
```

# Usage

Installing the package comes with a console command `generate_map`.

```
generate_map --help
usage: generate_map [-h] [--config-path CONFIG_PATH] [--output-config OUTPUT_CONFIG] [--output-dir OUTPUT_DIR] [--output-csv OUTPUT_CSV]
                    [--reset-config] [--only-update-config] [--print-date] [--print-config]
                    [--loglevel {debug,info,warning,error,fatal,critical}]

optional arguments:
  -h, --help            show this help message and exit
  --config-path CONFIG_PATH, -P CONFIG_PATH
                        The path to the config file or directory
  --output-config OUTPUT_CONFIG, -c OUTPUT_CONFIG
                        The path and name of the output config file
  --output-dir OUTPUT_DIR, -D OUTPUT_DIR
                        The path for all generated output
  --output-csv OUTPUT_CSV, -o OUTPUT_CSV
                        The path for the csv memory map
  --reset-config, -r    Do not copy previous non-generated mem map values
  --only-update-config, -u
                        Only updates config file without generating files
  --print-date, -d      prints the date in all headers
  --print-config, -p    Prints the config to stdout
  --loglevel {debug,info,warning,error,fatal,critical}
                        Python logger log level, defaults to "info"
```

Typically one would have a config fitting the [schema](memory_map_manager/data/mem_map_schema.json) and generate .c and .h files from it.

An [example](example_typedef.json) shows how to format and what the memory map will look like.
Note that only the `metadata`, `typedef`, and `bitfields` must be populated as the `memory_map` can be populated based on that information.


# Testing

Procedure for changes to example_typedef.json (please verify first)
```
python3 -m memory_map_manager.code_gen -P example_typedef.json -c example_typedef.json -u
```

To run the full test suite and linter use:
```
tox
```

To run just the test
```
python setup.py pytest
```

Reset regression test
```
python3 setup.py test --addopts --regtest-reset
```
