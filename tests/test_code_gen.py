# Copyright (c) 2018 Kevin Weiss, for HAW Hamburg  <kevin.weiss@haw-hamburg.de>
#
# This file is subject to the terms and conditions of the MIT License. See the
# file LICENSE in the top level directory for more details.
# SPDX-License-Identifier:    MIT
"""Tests Serial Driver implmentation in RIOT PAL."""
import os
import shutil


def rm_r(path):
    if os.path.isdir(path) and not os.path.islink(path):
        shutil.rmtree(path)
    elif os.path.exists(path):
        os.remove(path)


def test_cli_example_complex(script_runner):
    ret = script_runner.run('mmm-gen', '-p', 'examples/complex/mp1.yaml')
    assert ret.success
    assert 'SUCCESS' in ret.stdout
    ret = script_runner.run('mmm-gen', '-p', 'examples/complex/mp2.yaml')
    assert ret.success
    assert 'SUCCESS' in ret.stdout
    ret = script_runner.run('mmm-gen', '-p', 'examples/complex/sa.yaml')
    assert ret.success
    assert 'SUCCESS' in ret.stdout
    ret = script_runner.run('mmm-gen', '-p', 'examples/complex/sensor.yaml')
    assert ret.success
    assert 'SUCCESS' in ret.stdout


def test_cli_minimal(script_runner):
    rm_r('/tmp/gen')
    ret = script_runner.run('mmm-gen', '-p', 'examples/minimal/main.yaml')
    assert ret.success
    assert 'SUCCESS' in ret.stdout
    ret = script_runner.run('mmm-gen', '-p', 'examples/minimal/all_outputs.yaml')
    assert ret.success
    assert 'SUCCESS' in ret.stdout
    ret = script_runner.run('mmm-gen', '-p', 'examples/minimal/main.yaml', '-C')
    assert ret.success
    assert 'SUCCESS' in ret.stdout


def test_cli_example_full(script_runner):
    ret = script_runner.run('mmm-gen', '-p', 'examples/full/main.yaml')
    assert ret.success
    assert 'SUCCESS' in ret.stdout


def test_cli_example_philip(script_runner):
    ret = script_runner.run('mmm-gen', '-p', 'examples/philip/main.yaml')
    assert ret.success
    assert 'SUCCESS' in ret.stdout


def test_minimal_empty(script_runner):
    ret = script_runner.run('mmm-gen', '-p', 'tests/data/minimal_empty/main.yaml')
    assert ret.success
    assert 'SUCCESS' not in ret.stdout
