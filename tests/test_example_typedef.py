# Copyright (c) 2018 Kevin Weiss, for HAW Hamburg  <kevin.weiss@haw-hamburg.de>
#
# This file is subject to the terms and conditions of the MIT License. See the
# file LICENSE in the top level directory for more details.
# SPDX-License-Identifier:    MIT
"""Tests Serial Driver implmentation in RIOT PAL."""
from copy import deepcopy
import json
import difflib
import pytest
from memory_map_manager.config_import_export import import_config
from memory_map_manager.td_parser import update_typedefs
from memory_map_manager.mm_parser import parse_typedefs_to_mem_maps
from memory_map_manager.td_output_parser import parse_typedefs_to_h
from memory_map_manager.mm_output_parser import parse_mem_map_to_defaults_h
from memory_map_manager.mm_output_parser import parse_mem_map_to_map_v_c
from memory_map_manager.mm_output_parser import parse_mem_map_to_map_v_h
from memory_map_manager.mm_output_parser import parse_mem_map_to_defaults_c
from memory_map_manager.mm_output_parser import parse_mem_map_to_csv
from memory_map_manager.mm_output_parser import parse_mem_map_to_access_c


@pytest.fixture
def example_config():
    yield import_config('example_typedef.json')


# pylint: disable=W0621
def test_import_regression(regtest, example_config):
    """Tests the import from json against accepted input"""
    regtest.write(json.dumps(example_config, sort_keys=True, indent=4))


# pylint: disable=W0621
def test_updated_regression(regtest, example_config):
    """Tests the full transform of the config file against accepted value"""
    update_typedefs(example_config)
    parse_typedefs_to_mem_maps(example_config, True)
    regtest.write(json.dumps(example_config, sort_keys=True, indent=4))


# pylint: disable=W0621
def test_diff_generated_imported(regtest, example_config):
    """Tests to see if importing non-generated values works"""
    update_typedefs(example_config)
    generated_config = deepcopy(example_config)
    parse_typedefs_to_mem_maps(example_config, True)
    parse_typedefs_to_mem_maps(generated_config, False)
    imp_mm = json.dumps(example_config['mem_maps'], sort_keys=True, indent=4)
    gen_mm = json.dumps(generated_config['mem_maps'], sort_keys=True, indent=4)
    for outstr in difflib.unified_diff(imp_mm.splitlines(),
                                       gen_mm.splitlines(), n=0):
        last_str = outstr
    regtest.write(last_str)


# pylint: disable=W0621
def test_c_h_outputs(regtest, example_config):
    """Test to generated c and h stay the same."""
    update_typedefs(example_config)
    parse_typedefs_to_mem_maps(example_config, False)
    regtest.write(parse_typedefs_to_h(example_config))
    # regtest.write seems to have a bug with the rendering of 0xn, 0xm
    # as a result it is expected that we get something like 0x00, 0x????????
    regtest.write(parse_mem_map_to_access_c(example_config))
    regtest.write(parse_mem_map_to_map_v_c(example_config))
    regtest.write(parse_mem_map_to_map_v_h(example_config))
    regtest.write(parse_mem_map_to_defaults_h(example_config))
    regtest.write(parse_mem_map_to_defaults_c(example_config))


# pylint: disable=W0621
def test_csv_outputs(regtest, example_config):
    update_typedefs(example_config)
    parse_typedefs_to_mem_maps(example_config, True)
    for mem_map in example_config['mem_maps']:
        regtest.write(parse_mem_map_to_csv(mem_map))
