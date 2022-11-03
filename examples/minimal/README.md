This is an example of the bare minimum map requirements.
It contains the map, the map c_file outputs, and a simple C program to ensure that the c_file outputs can be used.

Note that the `CMake.txt` and `tests` have been manually created.
Also remember that the [schema](../../memory_map_manager/data/mm_map_cfg.json) states that unassigned default values of the maps will be 0.

# Usage

Regenerate the files with:
```
mmm-gen
```

Build the binaries (assuming CMake is setup):
```
cmake -S . -B build
cmake --build build/
```

Test the binaries:
```
cd build
ctest
cd ..
```

Verify the output manually:
```
./build/tests/test_0
```
