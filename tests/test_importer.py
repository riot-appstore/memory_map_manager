# Copyright (c) 2022 Kevin Weiss, for HAW Hamburg  <kevin.weiss@haw-hamburg.de>
#
# This file is subject to the terms and conditions of the MIT License. See the
# file LICENSE in the top level directory for more details.
# SPDX-License-Identifier:    MIT
"""Tests the importer for the memory map.

TODO:
- confirm overwrite works
"""
import os
import pathlib

import pytest
from jsonschema import ValidationError

from memory_map_manager import MMMImporter


def _fpath(fname):
    fdir = pathlib.Path(__file__).parent.resolve()
    return pathlib.PurePath(fdir, 'data/importer', fname + '.yaml')


def _importer_file(fname) -> MMMImporter:
    return MMMImporter(_fpath(fname))


@pytest.mark.parametrize("fname", ['base_dir_none',
                                   'base_dir_rel'])
def test_base_dir(fname):
    mmi = _importer_file(fname)
    assert mmi.mm_data is not None


@pytest.mark.skipif(os.environ.get('ACTIONS_CI') != '1',
                    reason='Requires specific path hard-coded for CI')
def test_abs():
    mmi = _importer_file('base_dir_abs')
    assert mmi.mm_data is not None


def test_init_none():
    mmi = MMMImporter()
    assert len(mmi._mm_files) == 0
    mmi.import_cfg_file(_fpath('base_dir_none'))
    assert mmi.mm_data is None
    assert len(mmi._mm_files) > 0


def test_full():
    mmi = _importer_file('full')
    assert len(mmi._mm_files) > 0
    assert mmi._base_dir == mmi.csv_dir
    assert mmi._base_dir + 'importer' == mmi.c_dir
    assert mmi.cfg_dir == '/tmp'
    assert mmi.prompt_conflicts is True
    assert mmi.overwrite_conflicts is False


def test_import_map_data():
    mmi = MMMImporter()
    mmi.import_map_data(_fpath('cfg_basic'))
    assert mmi.mm_data['metadata']['app_name'] == 'something'
    mmi.overwrite_conflicts = True
    mmi.import_map_data([_fpath('cfg_basic'), _fpath('cfg_basic_other')])
    assert mmi.mm_data['metadata']['app_name'] == 'something_else'


@pytest.mark.parametrize("prompt_input", ['y', 'n', ''])
def test_prompt_conflict(monkeypatch, prompt_input):
    mmi = MMMImporter()
    mmi.prompt_conflicts = True
    monkeypatch.setattr('builtins.input', lambda _: prompt_input)
    mmi.import_map_data([_fpath('cfg_basic'), _fpath('cfg_basic_other')])

    if prompt_input == 'y':
        assert mmi.mm_data['metadata']['app_name'] == 'something_else'
    else:
        assert mmi.mm_data['metadata']['app_name'] == 'something'

    mmi.overwrite_conflicts = True
    mmi.import_map_data([_fpath('cfg_basic'), _fpath('cfg_basic_other')])
    if prompt_input == 'y' or prompt_input == '':
        assert mmi.mm_data['metadata']['app_name'] == 'something_else'
    else:
        assert mmi.mm_data['metadata']['app_name'] == 'something'


def test_invalid_prompt_conflict(monkeypatch):
    mmi = MMMImporter()
    mmi.prompt_conflicts = True
    responses = iter(['invalid', ''])
    monkeypatch.setattr('builtins.input', lambda _: next(responses))
    mmi.import_map_data([_fpath('cfg_basic'), _fpath('cfg_basic_other')])
    assert mmi.mm_data['metadata']['app_name'] == 'something'


def test_error_conflict():
    mmi = MMMImporter()
    with pytest.raises(KeyError):
        mmi.import_map_data([_fpath('cfg_basic'), _fpath('cfg_basic_other')])


def test_error_missing_required():
    with pytest.raises(ValidationError):
        _importer_file('error_missing_required')


def test_error_undefined():
    with pytest.raises(ValidationError):
        _importer_file('error_undefined')
