# Copyright (c) 2018 Kevin Weiss, for HAW Hamburg  <kevin.weiss@haw-hamburg.de>
#
# This file is subject to the terms and conditions of the MIT License. See the
# file LICENSE in the top level directory for more details.
# SPDX-License-Identifier:    MIT
"""Tests Serial Driver implmentation in RIOT PAL."""
import json
import pytest
from memory_map_manager import MMMConfigParser


@pytest.fixture
def mcp() -> MMMConfigParser:
    return MMMConfigParser()


@pytest.fixture
def full_mcp() -> MMMConfigParser:
    data = {'bitfields': {'bf_1': {'elements': ['field_1', 'field_2']},
                          'bf_2': {'elements': [{'bits': 12, 'name': 'field_1'}]}},
              'defines': {'def_1': 3},
              'generated_maps': {'map_1': {'type': 'type_1'},
                                  'map_2': {'type': 'type_3'},
                                  'map_3': {'type': 'type_5'}},
              'metadata': {'app_name': 'simple_full', 'default_map': 'map_3'},
              'typedefs': {'type_1': {'elements': [{'default': 1,
                                                  'name': 'record_1',
                                                  'type': 'uint32_t'},
                                                  {'array_size': 2,
                                                  'default': 2,
                                                  'name': 'record_2',
                                                  'type': 'uint16_t'},
                                                  {'array_size': 'def_1',
                                                  'default': 'def_1',
                                                  'name': 'record_3',
                                                  'type': 'uint8_t'},
                                                  {'name': 'record_4', 'type': 'bf_1'},
                                                  {'array_size': 1,
                                                  'name': 'record_5',
                                                  'type': 'bf_1'},
                                                  {'array_size': 'def_1',
                                                  'name': 'record_6',
                                                  'type': 'bf_2'},
                                                  {'name': 'record_7',
                                                  'type': 'type_2'},
                                                  {'array_size': 4,
                                                  'name': 'record_8',
                                                  'type': 'type_2'},
                                                  {'array_size': 'def_1',
                                                  'name': 'record_9',
                                                  'type': 'type_2'}]},
                          'type_2': {'elements': ['record_1']},
                          'type_3': {'elements': [{'array_size': 2,
                                                  'name': 'record_1',
                                                  'type': 'type_1'}]},
                          'type_4': {'elements': [{'array_size': 2,
                                                  'name': 'record_1',
                                                  'type': 'uint16_t'}]},
                          'type_5': {'elements': [{'array_size': 3,
                                                  'name': 'record_1',
                                                  'type': 'type_4'}]}}}

    return MMMConfigParser(data)


@pytest.fixture
def min_data() -> dict:
    return {
        "metadata": {
            "app_name": "pytest"
        },
        "typedefs": {
            "td_1": {
                "elements": [
                    "record_1"
                ]
            }
        },
        "generated_maps": {
            "map_1": {
                "type": "td_1"
            }
        }
    }


def test_min_resolve_all(mcp: MMMConfigParser, min_data: dict):
    mcp.resolve_all_data(min_data)
    assert mcp.get_cfg()['metadata']['app_name'] == 'pytest'
    assert mcp.get_cfg()['maps']['map_1']['records'][0]['name'] == 'record_1'


@pytest.mark.parametrize("missing", ['metadata', 'generated_maps'])
def test_error_resolve_all(mcp: MMMConfigParser, min_data: dict, missing):
    del min_data[missing]
    with pytest.raises(KeyError):
        mcp.resolve_all_data(min_data)


def test_resolved_defs_int(mcp: MMMConfigParser):
    mcp.resolve_defines({'test': {'value': 1}})
    assert mcp.resolved_defs['test'] == 1


def test_resolved_defs_str(mcp: MMMConfigParser):
    mcp.resolve_defines({'test': {'value': '"str"'}})
    assert mcp.resolved_defs['test'] == '"str"'


def test_resolved_defs_nested(mcp: MMMConfigParser):
    data = {
        "def_1": {"value": "1"},
        "def_2": {"value": "def_3 + 2"},
        "def_3": {"value": "def_1 + 3"}
    }
    mcp.resolve_defines(data)
    mdef = mcp.resolved_defs
    assert mdef['def_1'] == 1
    assert mdef['def_3'] == 4
    assert mdef['def_2'] == 6


def test_error_resolved_defs(mcp: MMMConfigParser):
    data = {
        "def_1": {"value": '"1"'},
        "def_2": {"value": "def_3 + 2"},
        "def_3": {"value": "def_1 + 3"}
    }
    with pytest.raises(RecursionError):
        mcp.resolve_defines(data)


def test_bf_min(mcp: MMMConfigParser):
    data = {
        "bf_1": {"elements": ["field_1"]}
    }
    mcp.resolve_bitfields(data)
    bf1 = mcp.get_cfg()['bitfields']['bf_1']
    field1 = bf1['elements'][0]
    assert bf1['resolved_type'] == 'uint8_t'
    assert field1['name'] == 'field_1'
    assert field1['resolved_bit_offset'] == 0
    assert field1['resolved_bits'] == 1
    assert bf1['elements'][-1]['name'] == 'padding'


def test_bf_ref(mcp: MMMConfigParser):
    data = {
        "bf_1": {"elements": ["field_1"]},
        "bf_2": {
            "elements": [{"name": "field_2"}],
            "reference": "bf_1"
        }
    }
    mcp.resolve_bitfields(data)
    bfs = mcp.get_cfg()['bitfields']
    assert len(bfs) == 2
    ele2 = bfs['bf_2']['elements']
    assert ele2[0]['name'] == 'field_1'
    assert ele2[1]['name'] == 'field_2'
    assert ele2[1]['resolved_bit_offset'] == 1
    assert ele2[-1]['name'] == 'padding'


def test_bf_no_pad(mcp: MMMConfigParser):
    data = {
        'no_pad_8': {'elements': [{'bits': 5, 'name': 'field_1'},
                                  {'bits': 3, 'name': 'field_2'}]},
        'no_pad_16': {'elements': [{'bits': 12, 'name': 'field_1'},
                                   {'bits': 4, 'name': 'field_2'}]},
        'no_pad_32': {'elements': [{'bits': 15, 'name': 'field_1'},
                                   {'bits': 17, 'name': 'field_2'}]},
        'no_pad_64': {'elements': [{'bits': 31, 'name': 'field_1'},
                                   {'bits': 33, 'name': 'field_2'}]}
    }
    mcp.resolve_bitfields(data)
    for k, bf in mcp.get_cfg()['bitfields'].items():
        assert len(bf['elements']) == 2


def test_bf_with_types(mcp: MMMConfigParser):
    data = {
        'bf_w16': {'elements': ['field_1'], 'type': 'uint16_t'},
        'bf_w32': {'elements': ['field_1'], 'type': 'uint32_t'},
        'bf_w64': {'elements': ['field_1'], 'type': 'uint64_t'},
        'bf_w8': {'elements': ['field_1'], 'type': 'uint8_t'}
    }
    mcp.resolve_bitfields(data)
    for k, bf in mcp.get_cfg()['bitfields'].items():
        b_size = mcp.PRIMARIES[bf['type']] * 8
        assert bf['elements'][-1]['name'] == 'padding'
        assert bf['elements'][-1]['resolved_bit_offset'] == 1
        assert bf['elements'][-1]['resolved_bits'] == b_size - 1


def test_bf_defs(mcp: MMMConfigParser):
    def_data = {
        "def_val": {"value": 2}
    }
    mcp.resolve_defines(def_data)

    data = {
        'bf_1': {
            'elements': [
                {
                    "name": "field_1",
                    "bits": "def_val"
                },
            ]
        }
    }
    mcp.resolve_bitfields(data)
    bf_1 = mcp.get_cfg()['bitfields']['bf_1']
    assert bf_1['elements'][0]['resolved_bits'] == 2
    assert bf_1['elements'][0]['bits'] == 'def_val'


def test_error_bf_enum_conflict(mcp: MMMConfigParser):
    data = {'foo': {'elements': ['bar']}}

    with pytest.raises(KeyError):
        mcp.resolve_bitfields(data)
        mcp.resolve_enumerations(data)
        mcp.resolve_typedefs({'foo2': {'elements': ['bar2']}})


@pytest.mark.parametrize("bits", [0, 65])
def test_error_bf_invalid_bits(mcp: MMMConfigParser, bits):
    data = {
        "bf_1": {"elements": [{
            "name": "field_1",
            "bits": bits
        }]}
    }
    with pytest.raises(ValueError):
        mcp.resolve_bitfields(data)


def test_error_bf_bitoverflow(mcp: MMMConfigParser):
    data = {
        "bf_1": {
            "type": "uint8_t",
            "elements": [{
                "name": "field_1",
                "bits": 9
            }]
        }
    }
    with pytest.raises(ValueError):
        mcp.resolve_bitfields(data)


def test_error_bf_dup_ele(mcp: MMMConfigParser):
    data = {
        "bf_1": {
            "type": "uint8_t",
            "elements": [
                "field_1",
                "field_1"
            ]
        }
    }
    with pytest.raises(KeyError):
        mcp.resolve_bitfields(data)


def test_enum_min(mcp: MMMConfigParser):
    data = {'enum_1': {'elements': ['opt_1']}}
    mcp.resolve_enumerations(data)
    enu = mcp.get_cfg()['enums']['enum_1']
    opt = mcp.get_cfg()['enums']['enum_1']['elements'][0]
    assert opt['name'] == 'opt_1'
    assert opt['resolved_value'] == 0
    assert enu['resolved_type'] == mcp.default_type


def test_enum_type(mcp: MMMConfigParser):
    data = {'enum_1': {'elements': ['opt_1'], 'type': 'int16_t'}}
    mcp.resolve_enumerations(data)
    enu = mcp.get_cfg()['enums']['enum_1']
    assert enu['resolved_type'] == 'int16_t'


def test_enum_ref(mcp: MMMConfigParser):
    data = {'enum_1': {'elements': ['opt_1']},
            'enum_2': {'elements': ['opt_2'], 'reference': 'enum_1'}}
    mcp.resolve_enumerations(data)
    enu = mcp.get_cfg()['enums']['enum_2']['elements']
    assert enu[0]['name'] == 'opt_1'
    assert enu[1]['name'] == 'opt_2'
    assert enu[1]['resolved_value'] == 1


def test_enum_bitwise(mcp: MMMConfigParser):
    data = {
        "enum_1": {
            "bitwise": True,
            "elements": [
                "opt_1", "opt_2", "opt_3"
            ]
        }
    }
    mcp.resolve_enumerations(data)
    eles = mcp.get_cfg()['enums']['enum_1']['elements']
    assert eles[0]['resolved_value'] == 1 << 0
    assert eles[1]['resolved_value'] == 1 << 1
    assert eles[2]['resolved_value'] == 1 << 2


def test_enum_val(mcp: MMMConfigParser):
    data = {'enum_1': {'elements': [
        {'name': 'opt_1', 'value': 99},
        'opt_2',
        {'name': 'opt_3'},
        {'name': 'opt_4', 'value': 1},
        'opt_5']
    }}
    mcp.resolve_enumerations(data)
    eles = mcp.get_cfg()['enums']['enum_1']['elements']
    assert eles[0]['resolved_value'] == 99
    assert eles[1]['resolved_value'] == 100
    assert eles[2]['resolved_value'] == 101
    assert eles[3]['resolved_value'] == 1
    assert eles[4]['resolved_value'] == 2


def test_error_enum_dup_ele(mcp: MMMConfigParser):
    data = {'enum_1': {'elements': [
        "opt_1",
        "opt_1"
    ]}}
    with pytest.raises(KeyError):
        mcp.resolve_enumerations(data)


def test_error_enum_invalid_type(mcp: MMMConfigParser):
    data = {'enum_1': {'elements': ['opt_1'], 'type': 'float'}}
    with pytest.raises(ValueError):
        mcp.resolve_enumerations(data)


def test_error_enum_type_small(mcp: MMMConfigParser):
    data = {
        'enum_1':
        {
            'elements':
            [
                {
                    'name': 'opt_1', 'value': 257
                }
            ],
            'type': 'uint8_t'
        }
    }
    with pytest.raises(ValueError):
        mcp.resolve_enumerations(data)


def test_td_min(mcp: MMMConfigParser):
    data = {'td_1': {'elements': ['record_1']}}
    mcp.resolve_typedefs(data)
    rec = mcp.get_cfg()['typedefs'][0]['td_1']['elements'][0]
    assert rec['name'] == 'record_1'
    assert rec['resolved_type'] == mcp.default_type
    assert rec['resolved_offset'] == 0
    assert rec['resolved_total_size'] == mcp.PRIMARIES[mcp.default_type]
    assert rec['resolved_type_size'] == rec['resolved_total_size']
    _tmp = mcp.typedefs['td_1']['resolved_total_size']
    assert _tmp == rec['resolved_total_size']


def test_td_nested(mcp: MMMConfigParser):
    data = {'td_1': {'elements': ['record_1']},
            'td_2': {'elements': [{'name': 'record_1', 'type': 'td_3'}]},
            'td_3': {'elements': [{'name': 'record_1', 'type': 'td_1'}]}}

    mcp.resolve_typedefs(data)
    rec = mcp.typedefs['td_2']['elements'][0]
    assert rec['name'] == 'record_1'
    assert rec['resolved_type'] == 'td_3'
    _tmp = mcp.typedefs['td_1']['resolved_total_size']
    assert mcp.typedefs['td_2']['resolved_total_size'] == _tmp
    assert mcp.typedefs['td_3']['resolved_total_size'] == _tmp


def test_td_multi_ref(mcp: MMMConfigParser):
    data = {'atd_3': {'elements': ['record_3'], 'reference': 'btd_2'},
            'btd_2': {'elements': ['record_2'], 'reference': 'ctd_1'},
            'ctd_1': {'elements': ['record_1']}}

    mcp.resolve_typedefs(data)
    eles = mcp.typedefs['atd_3']['elements']
    assert eles[0]['name'] == 'record_1'
    assert eles[1]['name'] == 'record_2'
    assert eles[2]['name'] == 'record_3'
    _tmp = 3 * mcp.PRIMARIES[mcp.default_type]
    assert mcp.typedefs['atd_3']['resolved_total_size'] == _tmp


def test_td_ref(mcp: MMMConfigParser):
    data = {'td_1': {'elements': ['record_1']},
            'td_2': {'elements': ['record_2'], 'reference': 'td_1'}}
    mcp.resolve_typedefs(data)
    eles = mcp.typedefs['td_2']['elements']
    assert eles[0]['name'] == 'record_1'
    assert eles[1]['name'] == 'record_2'
    _tmp = 2 * mcp.typedefs['td_1']['resolved_total_size']
    assert mcp.typedefs['td_2']['resolved_total_size'] == _tmp


def test_td_array(mcp: MMMConfigParser):
    data = {'td_1': {'elements': [{'array_size': 2, 'name': 'record_1'}]}}
    mcp.resolve_typedefs(data)
    rec = mcp.typedefs['td_1']['elements'][0]
    tsize = mcp.PRIMARIES[mcp.default_type]

    assert mcp.typedefs['td_1']['resolved_total_size'] == tsize * 2
    assert rec['resolved_type_size'] == tsize
    assert rec['resolved_total_size'] == tsize * 2
    assert rec['array_size'] == 2


def test_td_with_bf(mcp: MMMConfigParser):
    data = {'td_1': {'elements': ['record_1', {'name': 'r_with_bf', 'type': 'bf_1'}]}}
    bf_data = {'bf_1': {'elements': ['field_1']}}

    mcp.resolve_bitfields(bf_data)
    mcp.resolve_typedefs(data)
    bf_size = mcp.get_cfg()['bitfields']['bf_1']['resolved_type_size']
    recs = mcp.typedefs['td_1']['elements']
    tot_size = recs[0]['resolved_total_size']

    assert mcp.typedefs['td_1']['resolved_total_size'] == tot_size + bf_size
    assert recs[1]['name'] == 'r_with_bf'
    assert recs[1]['type'] == 'bf_1'


def test_td_with_enum(mcp: MMMConfigParser):
    data = {'td_1': {'elements': ['record_1', {'name': 'r_with_enum', 'type': 'enum_1'}]}}
    enum_data = {'enum_1': {'elements': ['opt_1']}}

    mcp.resolve_enumerations(enum_data)
    mcp.resolve_typedefs(data)
    enu1 = mcp.get_cfg()['enums']['enum_1']
    enum_size = enu1['resolved_type_size']
    recs = mcp.typedefs['td_1']['elements']
    tot_size = recs[0]['resolved_total_size']

    assert mcp.typedefs['td_1']['resolved_total_size'] == tot_size + enum_size
    assert recs[1]['name'] == 'r_with_enum'
    assert recs[1]['enum'] == 'enum_1'
    assert recs[1]['resolved_type'] == enu1['resolved_type']


def test_td_stuct_align(mcp: MMMConfigParser):
    mcp._struct_align = 64
    data = {'td_1': {'elements': ['record_1']}}
    mcp.resolve_typedefs(data)
    eles = mcp.typedefs['td_1']['elements']
    td1 = mcp.typedefs['td_1']
    assert eles[0]['name'] == 'record_1'
    assert eles[1]['name'] == 'padding'
    assert td1['resolved_total_size'] == mcp._struct_align


def test_td_stuct_align_fit(mcp: MMMConfigParser):
    mcp._struct_align = 4
    data = {'td_1': {'elements': [{'name': 'record_1', 'type': 'uint32_t'}]}}
    mcp.resolve_typedefs(data)
    eles = mcp.typedefs['td_1']['elements']
    td1 = mcp.typedefs['td_1']
    assert len(eles) == 1

def test_td_total_size_overwrite_stuct_align(mcp: MMMConfigParser):
    mcp._struct_align = 128
    data = {'td_1': {'elements': [{'name': 'record_1', 'type': 'uint32_t'}], 'total_size': 4}}
    mcp.resolve_typedefs(data)
    assert len(mcp.typedefs['td_1']['elements']) == 1


def test_td_align(mcp: MMMConfigParser):
    mcp._align = 4
    data = {'td_1': {'elements': [{'name': 'record_1', 'type': 'uint8_t'},
                                  {'name': 'record_2', 'type': 'uint16_t'},
                                  {'name': 'record_3', 'type': 'uint32_t'},
                                  {'name': 'record_4', 'type': 'uint64_t'},
                                  {'array_size': 3, 'name': 'record_5', 'type': 'uint8_t'}]}}
    mcp.resolve_typedefs(data)

    eles = mcp.typedefs['td_1']['elements']
    assert eles[0]['name'] == 'record_1'
    assert eles[1]['name'] == 'padding_0'
    assert eles[1]['resolved_total_size'] == 3
    assert eles[2]['name'] == 'record_2'
    assert eles[3]['name'] == 'padding_1'
    assert eles[3]['resolved_total_size'] == 2
    assert eles[4]['name'] == 'record_3'
    assert eles[5]['name'] == 'record_4'
    assert eles[6]['name'] == 'record_5'
    assert eles[7]['name'] == 'padding_2'


def test_td_total_size(mcp: MMMConfigParser):
    data = {'td_1': {'elements': ['record_1'], 'total_size': 8}}
    mcp.resolve_typedefs(data)
    eles = mcp.typedefs['td_1']['elements']
    td1 = mcp.typedefs['td_1']
    assert eles[0]['name'] == 'record_1'
    assert eles[1]['name'] == 'padding'
    assert td1['resolved_total_size'] == td1['total_size']


def test_td_total_size_eq(mcp: MMMConfigParser):
    data = {'td_1': {'elements': [{'name': 'record_1', 'type': 'uint32_t'}], 'total_size': 4}}
    mcp.resolve_typedefs(data)
    eles = mcp.typedefs['td_1']['elements']
    assert len(eles) == 1


def test_error_td_bf_name_conflict(mcp: MMMConfigParser):
    data = {'foo': {'elements': ['bar']}}

    with pytest.raises(KeyError):
        mcp.resolve_bitfields(data)
        mcp.resolve_typedefs(data)


def test_error_td_enum_name_conflict(mcp: MMMConfigParser):
    data = {'foo': {'elements': ['bar']}}

    with pytest.raises(KeyError):
        mcp.resolve_enumerations(data)
        mcp.resolve_typedefs(data)


def test_error_td_circ(mcp: MMMConfigParser):
    data = {'td_1': {'elements': [{'name': 'record_1', 'type': 'td_2'}]},
            'td_2': {'elements': [{'name': 'record_2', 'type': 'td_1'}]}}
    with pytest.raises(RecursionError):
        mcp.resolve_typedefs(data)


def test_error_td_circ_ref(mcp: MMMConfigParser):
    data = {'td_1': {'elements': ['record_1'], 'reference': 'td_2'},
            'td_2': {'elements': ['record_2'], 'reference': 'td_1'}}
    with pytest.raises(RecursionError):
        mcp.resolve_typedefs(data)


def test_td_dup_ele(mcp: MMMConfigParser):
    data = {'td_1': {'elements': ['record_1', 'record_1']}}
    with pytest.raises(KeyError):
        mcp.resolve_typedefs(data)


@pytest.mark.parametrize("total_size", [2, 0])
def test_error_td_total_size(mcp: MMMConfigParser, total_size):
    data = {
        'td_1': {
            'elements': [
                {
                    'name': 'record_1',
                    'type': 'uint32_t'
                }
            ],
            'total_size': total_size
        }
    }
    with pytest.raises(ValueError):
        mcp.resolve_typedefs(data)


def test_map_min(mcp: MMMConfigParser):
    """Resolve a minimum map example.

    This should be the minimal amount of data for a map to be correctly
    generated.
    """
    data = {'generated_maps': {'map_1': {'type': 'type_1'}},
            'metadata': {'app_name': 'minimal'},
            'typedefs': {'type_1': {'elements': ['record_1']}}}
    mcp.resolve_all_data(data)
    assert 'map_1' in mcp.maps


def test_map_simple_full(regtest, full_mcp: MMMConfigParser):

    maps = full_mcp.get_cfg()['maps']
    for mapname, mmap in maps.items():
        del mmap['compressed_records']
    regtest.write(json.dumps(maps, sort_keys=True, indent=2))


def test_map_hash(full_mcp: MMMConfigParser):
    meta = full_mcp.get_cfg()['metadata']
    fh = meta['full_hash']
    fwh = meta['fw_hash']
    swh = meta['sw_hash']
    full_mcp.maps['map_1'][0]['only_full_hash'] = 'will_be_changed'
    full_mcp._resolve_hashes()
    assert meta['full_hash'] != fh
    assert meta['fw_hash'] == fwh
    assert meta['sw_hash'] == swh

    full_mcp.maps['map_1'][0]['description'] = 'sw_will_be_changed'
    full_mcp._resolve_hashes()
    assert meta['fw_hash'] == fwh
    assert meta['sw_hash'] != swh

    full_mcp.maps['map_1'][0]['name'] = 'allwillbechanged'
    full_mcp._resolve_hashes()
    assert meta['fw_hash'] != fwh


def test_map_access_perm(regtest, mcp: MMMConfigParser):
    data = {'generated_maps': {'map_1': {'type': 'td_1'}},
            'metadata': {'app_name': 'access',
                        'permission_users': ['basic', 'advanced', 'god']},
            'typedefs': {'td_1': {'elements': [{'name': 'record_1',
                                                'write_permission': 0x8,
                                                'read_permission': 0xF},
                                                {'name': 'record_2',
                                                'write_permission': 'advanced',
                                                'read_permission': 'basic'},
                                                {'name': 'record_3',
                                                'write_permission': ['advanced', 'god'],
                                                'read_permission': None},
                                                {'name': 'record_4'}]}}}
    mcp.resolve_all_data(data)
    records = []
    keys = ['name', 'write_permission', 'read_permission', 'resolved_access']

    for record in mcp.get_cfg()['maps']['map_1']['records']:
        records.append({k: v for k, v in record.items() if k in keys})
    regtest.write(json.dumps(records, sort_keys=True, indent=2))


def test_map_scaled_defined_default(mcp: MMMConfigParser, min_data):

    data = {'metadata': {'app_name': 'test'},
            'bitfields': {'bf_1': {'elements': [{'bits': 2,
                                                'default': 16,
                                                'name': 'field_1',
                                                'scaling_factor': 8}]}},
            'defines': {'def_1': {'value': 10}},
            'generated_maps': {'map_1': {'type': 'td_1'}},
            'typedefs': {'td_1': {'elements': [{'default': 0.1,
                                                'name': 'record_1',
                                                'scaling_factor': 0.1},
                                                {'default': 10.1,
                                                'name': 'record_2',
                                                'scaling_factor': '10.1/2',
                                                'type': 'float'},
                                                {'name': 'record_3', 'type': 'bf_1'},
                                                {'default': 'def_1',
                                                'name': 'record_4',
                                                'scaling_factor': 'def_1'}]}}}


    mcp.resolve_all_data(data)
    assert mcp.maps['map_1'][0]['resolved_default'] == 0.1
    assert mcp.maps['map_1'][0]['resolved_scaled_default'] == 1
    assert mcp.maps['map_1'][1]['resolved_default'] == 10.1
    assert mcp.maps['map_1'][1]['resolved_scaled_default'] == 2.0
    assert 'resolved_scaled_min' not in mcp.maps['map_1'][1]
    assert mcp.maps['map_1'][2]['resolved_scaled_default'] == 2
    assert mcp.maps['map_1'][4]['resolved_scaling_factor'] == 10
    assert mcp.maps['map_1'][4]['resolved_scaled_default'] == 1


def test_map_inherit_specials(regtest, mcp: MMMConfigParser):
    data = {'bitfields': {'bf_1': {'elements': [{'name': 'field_1',
                                                 'overwrite_special': 15,
                                                 'special_15': 15},
                                                'field_2'],
                                   'overwrite_special': 14,
                                   'special_14': 14}},
            'generated_maps': {'map_1': {'type': 'td_1'},
                               'map_2': {'type': 'td_2'},
                               'map_3': {'type': 'td_3'}},
            'metadata': {'app_name': 'inherit_special'},
            'typedefs': {'td_1': {'elements': [{'name': 'record_1',
                                                'overwrite_special': 0,
                                                'special_0': 0},
                                               'record_2'],
                                  'overwrite_special': 1,
                                  'special_1': 1},
                         'td_2': {'elements': [{'name': 'record_3',
                                                'overwrite_special': 3,
                                                'special_3': 3,
                                                'type': 'td_1'},
                                               {'array_size': 2,
                                                'name': 'record_4',
                                                'overwrite_special': 4,
                                                'special_4': 4,
                                                'type': 'td_1'},
                                               'record_5',
                                               {'name': 'record_6',
                                                'overwrite_special': 6,
                                                'special_6': 6,
                                                'type': 'bf_1'},
                                               {'array_size': 2,
                                                'name': 'record_7',
                                                'overwrite_special': 7,
                                                'special_7': 7,
                                                'type': 'bf_1'}],
                                  'overwrite_special': 2,
                                  'special_2': 2},
                         'td_3': {'elements': [{'name': 'record_9',
                                                'overwrite_special': 9,
                                                'special_9': 9,
                                                'type': 'td_2'},
                                               {'array_size': 2,
                                                'name': 'record_10',
                                                'overwrite_special': 10,
                                                'special_5': 10,
                                                'type': 'td_2'},
                                               'record_11',
                                               {'name': 'record_12',
                                                'overwrite_special': 12,
                                                'special_12': 12,
                                                'type': 'bf_1'},
                                               {'array_size': 2,
                                                'name': 'record_13',
                                                'overwrite_special': 13,
                                                'special_13': 13,
                                                'type': 'bf_1'}],
                                  'overwrite_special': 8,
                                  'special_8': 8}}}
    mcp.resolve_all_data(data)
    test_vals = []
    drop_keys = ['map_offset', 'read_permission', 'write_permission',
                 'use_bitfields','use_defines', 'use_enums', 'writable',
                 'readable', 'description']

    # Drop data that is not useful for testing
    for mname in mcp.maps:
        for record in mcp.maps[mname]:
            record = record.copy()
            for k in list(record.keys()):
                if k.startswith('resolved') or k in drop_keys:
                    del record[k]
            record['map'] = mname
            test_vals.append(record)

    regtest.write(json.dumps(test_vals, sort_keys=True, indent=2))


def test_error_map_missing_perm(mcp: MMMConfigParser):
    data = {'generated_maps': {'map_1': {'type': 'td_1'}},
            'metadata': {'app_name': 'missing_permission'},
            'typedefs': {'td_1': {'elements': [{'name': 'record_1',
                                                'read_permission': 'missing'}]}}}
    with pytest.raises(KeyError):
        mcp.resolve_all_data(data)

def test_error_map_invalid_perm(mcp: MMMConfigParser):
    data = {'generated_maps': {'map_1': {'type': 'td_1'}},
            'metadata': {'app_name': 'missing_permission'},
            'typedefs': {'td_1': {'elements': [{'name': 'record_1',
                                                'read_permission': 0x10}]}}}
    with pytest.raises(ValueError):
        mcp.resolve_all_data(data)


def test_error_map_missing_type(mcp: MMMConfigParser):
    with pytest.raises(KeyError):
        mcp.resolve_maps({'map_1': {'type': 'missing'}})


def test_error_map_missing_type2(mcp: MMMConfigParser):
    with pytest.raises(KeyError):
        mcp.typedefs = {'missing': {'elements': [{'resolved_type': 'miss'}]}}
        mcp.resolve_maps({'map_1': {'type': 'missing'}})


def test_ovr_min(mcp: MMMConfigParser):
    data = {'generated_maps': {'map_1': {'type': 'type_1'}},
            'metadata': {'app_name': 'minimal'},
            'overrides': {'record_1': {'description': 'overridden'}},
            'typedefs': {'type_1': {'elements': [{'description': 'to override',
                                                  'name': 'record_1'}]}}}

    mcp.resolve_all_data(data)
    assert mcp.maps['map_1'][0]['description'] == 'overridden'


def test_ovr_default(mcp: MMMConfigParser):
    data = {'generated_maps': {'map_1': {'type': 'type_1'}},
            'metadata': {'app_name': 'minimal'},
            'overrides': {'record_1[0]': {'default': 2}},
            'typedefs': {'type_1': {'elements': [{'default': 1,
                                                  'name': 'record_1',
                                                  'array_size': 2},
                                                ]}}}

    mcp.resolve_all_data(data)
    assert mcp.maps['map_1'][0]['default'] == 2
    assert mcp.maps['map_1'][0]['default_changed'] == True
    assert mcp.maps['map_1'][1]['default'] == 1


def test_ovr_scaled_defined_default(mcp: MMMConfigParser, min_data):
    rec_1 = {'name': 'record_1'}
    rec_1['array_size'] = 3
    rec_1['scaling_factor'] = 1
    rec_1['default'] = 'def_1'
    rec_1['min'] = 1
    rec_1['max'] = 100
    min_data['typedefs']['td_1']['elements'][0] = rec_1
    min_data['defines'] = {'def_1': 10}
    min_data['overrides'] = {'record_1[1]': {'scaling_factor': 0.1},
                             'record_1[2]': {'scaling_factor': 'def_1 / 2'}
                            }
    mcp.resolve_all_data(min_data)
    assert mcp.maps['map_1'][0]['resolved_default'] == 10
    assert mcp.maps['map_1'][0]['resolved_scaled_default'] == 10
    assert mcp.maps['map_1'][1]['resolved_default'] == 10
    assert mcp.maps['map_1'][1]['resolved_scaled_default'] == 100
    assert mcp.maps['map_1'][1]['resolved_scaled_min'] == 10
    assert mcp.maps['map_1'][1]['resolved_scaled_max'] == 1000
    assert mcp.maps['map_1'][2]['resolved_scaled_default'] == 2
    assert mcp.maps['map_1'][2]['resolved_scaled_min'] == 0
    assert mcp.maps['map_1'][2]['resolved_scaled_max'] == 20


def test_ovr_regex(mcp: MMMConfigParser):
    data = {'generated_maps': {'map_1': {'type': 'type_1'}},
            'metadata': {'app_name': 'minimal'},
            'overrides': {'r"record_1\\[\\d+\\]"': {'description': 'overridden'},
                          'record_1[2]': {'description': 'specific override'}},
            'typedefs': {'type_1': {'elements': [{'array_size': 3,
                                                  'description': 'to override',
                                                  'name': 'record_1'}]}}}

    mcp.resolve_all_data(data)
    assert mcp.maps['map_1'][0]['description'] == 'overridden'
    assert mcp.maps['map_1'][1]['description'] == 'overridden'
    assert mcp.maps['map_1'][2]['description'] == 'specific override'


@pytest.mark.parametrize("record", ['r"no_match\\[\\d+\\]"',
                                      'no_match'])
def test_ovr_missing(mcp: MMMConfigParser, record):
    data = {'generated_maps': {'map_1': {'type': 'type_1'}},
            'metadata': {'app_name': 'minimal'},
            'overrides': {record: {'description': 'overridden'}},
            'typedefs': {'type_1': {'elements': [{'name': 'record_1'}]}}}
    with pytest.raises(KeyError):
        mcp.resolve_all_data(data)


def test_ovr_empty(mcp: MMMConfigParser):
    data = {'generated_maps': {'map_1': {'type': 'type_1'}},
            'metadata': {'app_name': 'minimal'},
            'overrides': {'record_1': {'description': 'something'}},
            'typedefs': {'type_1': {'elements': [{'name': 'record_1'}]}}}
    mcp.resolve_all_data(data)
    assert mcp.maps['map_1'][0]['description'] == 'something'


def test_meta_min(mcp: MMMConfigParser):
    mcp.resolve_metadata({'app_name': 'minimal'})
    meta = mcp.get_cfg()['metadata']
    assert meta['app_name'] == 'minimal'
    assert meta['version'] == '0.0.0'
    assert not meta['resolved_permission_users']
    assert mcp._align == None


def test_meta_full(mcp: MMMConfigParser):
    data = {'align': 4,
            'app_name': 'full',
            'default_map': 'map_1',
            'default_type': 'uint16_t',
            'struct_align': 8,
            'version': '0.0.1'}
    mcp.resolve_metadata(data)
    meta = mcp.get_cfg()['metadata']
    assert meta['app_name'] == 'full'
    assert mcp._align == 4
    assert mcp._struct_align == 8
    assert mcp.default_type == 'uint16_t'


def test_error_meta_default_map_conflict(mcp: MMMConfigParser):
    data = {'generated_maps': {'map_1': {'type': 'type_1'}},
            'metadata': {'app_name': 'full',
                         'default_map': 'map_missing'},
            'typedefs': {'type_1': {'elements': ['record_1']}}}
    with pytest.raises(KeyError):
        mcp.resolve_all_data(data)

