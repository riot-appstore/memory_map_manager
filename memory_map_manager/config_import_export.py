#!/usr/bin/env python3
# Copyright (c) 2018 Kevin Weiss, for HAW Hamburg  <kevin.weiss@haw-hamburg.de>
#
# This file is subject to the terms and conditions of the MIT License. See the
# file LICENSE in the top level directory for more details.
# SPDX-License-Identifier:    MIT
"""This module contains imports and exports the config file"""
import os
import json
from logging import debug, info
from pprint import pformat
from jsonschema import validate


_PATH_TO_SCHEMA = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                               "data/mem_map_schema.json")


def import_config(config_path):
    """Imports target config from file or directory."""
    info("Searching for config in %r", config_path)
    config = _import_type_check(config_path)
    if 'mem_maps' not in config:
        config['mem_maps'] = []
    if 'bitfields' not in config:
        config['bitfields'] = []
    debug("Imported:\n%s", pformat(config))
    return config


def _find_config_file_in_dir(config_path):
    debug("Searching directory for config file")
    for fname in os.listdir(config_path):
        if fname.endswith('.json'):
            info("Found %r config file in %r", fname, config_path)
            return os.path.join(config_path, fname)
        debug("%r not valid file", fname)
    raise FileNotFoundError("No config file in {}".format(config_path))


def _import_type_check(config_path):
    if config_path.endswith('.json'):
        return _import_config_from_json(config_path)
    return _import_config_from_json(_find_config_file_in_dir(config_path))


def _import_config_from_json(config_path):
    info("Importing %r", config_path)
    with open(config_path) as config_f:
        config = json.load(config_f)
    with open(_PATH_TO_SCHEMA) as schema_f:
        schema = json.load(schema_f)
    validate(config, schema)
    return config


def export_config(config, config_path):
    """Exports config file to target path."""
    with open(_PATH_TO_SCHEMA) as schema_f:
        schema = json.load(schema_f)
    validate(config, schema)
    if not config_path.endswith('.json'):
        config_path = _find_config_file_in_dir(config_path)
    with open(config_path, "w") as config_f:
        json.dump(config, config_f, sort_keys=True, indent=4)
