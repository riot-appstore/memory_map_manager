# `memory_map_manager`

The Memory Map Manager (MMM) generates code and documentation for embedded
device parameters intended for external interfaces.

## Motivation

Embedded systems typically run on constrained systems, providing some sort
of access to more powerful machines. A number of parameters can be read (such as
a temperature from a sensor) or written (such as the intended state of a light).
These amount of parameters and complexity can grow and change over the
development cycle of the device. Every parameter needs to not only be available
in the embedded device but also all the external interfaces as well.
If this information is not coordinated it can lead to human error and extra
development time. There are solutions available that helps with that, however,
they typically don't operate under the asymmetric nature of embedded vs host
computer capabilities or end of being very complex requiring large stacks in
order to use.

## Solution

The MMM generates simple C code that allows both named parameter access via
typedef structs and byte offset access. Decoding of these parameters are done
on the host, taking advantage of asymmetric computational resources of host vs.
device. The embedded device only needs to expose a way to read or write an
offset and size.

## Installation

_As this is a "console application" one can use a `venv` or `pipx` instead of pip._

Stable versions can be installed with:
```
pip install memory-map-manager
```

## Generating with the MMM

Installing the package comes with a console command `mmm-gen`.

```
usage: mmm-gen [-h] [--cfg-path CFG_PATH] [--clean]
               [--loglevel {debug,info,warning,error,fatal,critical}]

optional arguments:
  -h, --help            show this help message and exit
  --cfg-path CFG_PATH, -p CFG_PATH
                        the path to the memory map manager configuration importer.
  --clean, -C           clean the generated directories before generation. be careful!
  --loglevel {debug,info,warning,error,fatal,critical}
                        python logger log level, defaults to "info"
```

There are a number of examples available coming with the generation
configurations and the map configurations.

To run the minimal example run:
```
mmm-gen -p examples/minimal/main.yaml
```

This generates C files, csv files, and the configuration outputs.

## Writing a Custom Map

Along with the examples of maps there are schemas available that document the
capabilities.

There are two files that are needed:
- a [generation configuration](memory_map_manager/data/mm_gen_cfg.json) that
specifies generation information such as input configuration files and output directories. The default file is assumed to be `main.yaml`
- a [map configuration](memory_map_manager/data/mm_map_cfg.json) that specifies
the parameters in the map.
