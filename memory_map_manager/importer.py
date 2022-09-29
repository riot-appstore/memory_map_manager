# coding=utf-8
# Copyright (c) 2022 Kevin Weiss, for HAW Hamburg  <kevin.weiss@haw-hamburg.de>
#
# This file is subject to the terms and conditions of the MIT License. See the
# file LICENSE in the top level directory for more details.
# SPDX-License-Identifier:    MIT
"""Imports configurations and map info."""
from json import load
import logging
from os import path

from jsonschema import validate
from yaml import safe_load


_PATH_TO_IMPORT_SCHEMA = path.join(path.dirname(path.realpath(__file__)),
                                   "data/mm_gen_cfg.json")
_PATH_TO_INPUT_CONFIG_SCHEMA = path.join(path.dirname(path.realpath(__file__)),
                                         "data/mm_map_cfg.json")


class MMMImporter():
    """Memory map manager importer."""

    def __init__(self, cfg_file=None):
        """Instantiate the importer with a configuration file."""
        self.logger = logging.getLogger(self.__class__.__name__)
        """Logger the this class."""

        self.mm_data = None
        """The data from the imported memory maps."""

        self.c_dir = None
        """Directory to generate c files."""

        self.csv_dir = None
        """Directory to generate csv files for documentation."""

        self.cfg_dir = None
        """Directory to raw configuration files."""

        self.prompt_conflicts = False
        """Use console to confirm if a conflict should be overwritten."""

        self.overwrite_conflicts = False
        """Overwrite conflicts by default."""

        self._mm_files = []
        self._base_dir = None

        if cfg_file:
            self.import_cfg_file(cfg_file)
            self.import_map_data()

    def _get_fpath(self, fpath):
        if fpath is None:
            return None
        if not path.isabs(fpath):
            if fpath == '.':
                return self._base_dir
            return path.join(self._base_dir, fpath)
        return fpath

    def import_cfg_file(self, cfg_file):
        """Import and parse the main configuration file.

        This file contains all the parameters such as other files and export
        directories when running the configuration generation.
        """
        with open(cfg_file, 'r', encoding="utf-8") as fhandle:
            cfg_data = fhandle.read()
        cfg = safe_load(cfg_data)
        with open(_PATH_TO_IMPORT_SCHEMA, encoding="utf-8") as schema_f:
            schema = load(schema_f)
        validate(cfg, schema)

        abs_main = path.dirname(path.realpath(cfg_file))
        cfg_wd = cfg.get('base_dir', abs_main)
        if not path.isabs(cfg_wd):
            cfg_wd = path.join(abs_main, cfg_wd)
        self._base_dir = cfg_wd

        for fname in cfg['files']:
            self._mm_files.append(self._get_fpath(fname))

        self.c_dir = self._get_fpath(cfg.get('c_dir', None))
        self.csv_dir = self._get_fpath(cfg.get('csv_dir', None))
        self.cfg_dir = self._get_fpath(cfg.get('cfg_dir', None))
        self.prompt_conflicts = cfg.get('prompt_conflicts', False)
        self.overwrite_conflicts = cfg.get('overwrite_conflicts', False)

    def import_map_data(self, map_files=None):
        """Imports the map data based on the info from the cfg file.

        This brings in a handles conflicting or overridable data for the maps.
        """
        if map_files is None:
            map_files = self._mm_files
        elif not isinstance(map_files, list):
            map_files = [map_files]
        mm_data = {}
        for map_file in map_files:
            with open(map_file, 'r', encoding="utf-8") as yaml_files:
                data = safe_load(yaml_files)
            with open(_PATH_TO_INPUT_CONFIG_SCHEMA,
                      encoding="utf-8") as schema_f:
                schema = load(schema_f)
            validate(data, schema)
            for key, val in data.items():
                mm_data.setdefault(key, []).append(val)

        # We check all the files then have a structure like:
        # typedefs:
        #   - type_1: ...
        #     type_2: ...
        #   - other_file_type: ...
        #     type_1: ...
        # metadata:
        #   - app_name: from_file_1
        #   - app_name: from_file_2
        # ...
        for cfg_type in mm_data.copy():
            merged_dict = {}
            for new_dict in mm_data[cfg_type]:
                for key in new_dict:
                    self._check_dict_conflict(merged_dict, new_dict, key)
            mm_data[cfg_type] = merged_dict
        # Now we merge all the conflict first level nested keys to get:
        # typedefs:
        #   type_1: ... # Depending on settings or user selection
        #   type_2: ...
        #   other_file_type: ...
        # metadata:
        #   app_name: from_file_1 # Depending on settings or user selection
        # ...
        self.mm_data = mm_data

    def _check_dict_conflict(self, known: dict, new: dict, key):
        """Try to change and resolve any conflicts of keys.

        Depending on the settings the conflict will either overwrite, prompt
        or throw an exception.
        """
        def _prompt(owc, key, cu_val, ow_val):
            while True:
                print(f'Conflict detected for {key}: {cu_val}')
                if owc:
                    inp = input(f'Overwrite with {ow_val} [Y/n]? ') or 'Y'
                else:
                    inp = input(f'Overwrite with {ow_val} [y/N]? ') or 'N'
                if inp.upper() == 'Y':
                    return ow_val
                if inp.upper() == 'N':
                    return cu_val
                print("Invalid selection")
        if key in known:
            if self.prompt_conflicts:
                known[key] = _prompt(self.overwrite_conflicts,
                                     key, known[key], new[key])
            else:
                if self.overwrite_conflicts:
                    known[key] = new[key]
                else:
                    raise KeyError(f'Conflicting configuration {key}: '
                                   f'{known[key]} with new value {new[key]}!')
        else:
            known[key] = new[key]
