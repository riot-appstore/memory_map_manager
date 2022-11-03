# coding=utf-8
# Copyright (c) 2022 Kevin Weiss, for HAW Hamburg  <kevin.weiss@haw-hamburg.de>
#
# This file is subject to the terms and conditions of the MIT License. See the
# file LICENSE in the top level directory for more details.
# SPDX-License-Identifier:    MIT
"""Parses input data to full memory map data."""
from copy import deepcopy
import logging
import re

from memory_map_manager.json_sem_hash import get_json_sem_hash


class MMMConfigParser():
    """Parse and calculate internal memory map from config."""

    PRIMARIES = {'uint8_t': 1, 'int8_t': 1, 'uint16_t': 2, 'int16_t': 2,
                 'uint32_t': 4, 'int32_t': 4, 'uint64_t': 8, 'int64_t': 8,
                 'char': 1, 'float': 4, 'double': 8}
    """List of accepted primary data types."""

    RESERVED_KEYS = [
        'name',
        'resolved_type',
        'resolved_array_size',
        'resolved_type_size',
        'resolved_total_size',
        'resolved_offset',
        'resolved_type',
        'type',
        'array_size',
        'type_size',
        'total_size',
        'bits',
        'description',
        'elements',
        'deps'
    ]
    """List of keys that should be inherited by other properties.

    This is either because they are generated parameters or have special
    functions when generating.
    """

    _DEFAULT_TYPE = 'uint32_t'

    def __init__(self, mm_data=None):
        """Instantiate the parser and run if data available."""
        self.logger = logging.getLogger(self.__class__.__name__)
        """Logger the this class."""

        self._align = None
        """Member align value."""

        self._struct_align = None
        """Struct align value."""

        self._dflt_map = None
        """Default map to use."""

        self.default_type = self._DEFAULT_TYPE
        """The default type to use when no type is specified in cfg."""

        self.resolved_defs = {}
        """Resolved defines, key (define name) and val (int)."""

        self._defines = {}
        self._enums = {}
        """Holder of enumerations."""

        self._bfs = {}
        """Holder of bitfields."""

        self._tdo = []
        """List of evaluated typedef order."""

        self.typedefs = {}
        """Typedefs used for evaluation and map creation."""

        self._meta = {}
        """Holder of metadata."""

        self.maps = {}
        """Collection of records of each map.

        self.map[map_name][record_idx][record_properties]
        """

        self._maps_types = {}
        self._c_maps = {}
        """Compressed maps.

        The a copy of the records but with the arrays compressed instead of
        expanded.
        """

        self._cur_map = None
        """Current map holder for recursive eval of records."""

        self._record_prefix = None
        self._rec_parent_fields = []
        self._compress_array = []
        self._compress_uid = 1
        self._map_offset = 0
        if mm_data:
            self.resolve_all_data(mm_data)

    def _resolve_hashes(self):
        fw_keys = [
            'name',
            'resolved_type',
            'resolved_array_size',
            'resolved_type_size',
            'resolved_total_size',
            'resolved_offset',
            'resolved_type'
        ]
        sw_keys = [
            'name',
            'resolved_type',
            'resolved_array_size',
            'resolved_type_size',
            'resolved_total_size',
            'resolved_offset',
            'resolved_type',
            'description'
        ]
        self._meta['full_hash'] = get_json_sem_hash(self.maps)
        fw_map = {}
        sw_map = {}
        for map_key, records in self.maps.items():
            fw_map[map_key] = []
            sw_map[map_key] = []
            for record in records:
                fw_records = {}
                for key in fw_keys:
                    if key in record:
                        fw_records[key] = record[key]
                fw_map[map_key].append(fw_records)

                sw_records = {}
                for key in sw_keys:
                    if key in record:
                        sw_records[key] = record[key]
                sw_map[map_key].append(sw_records)
        self._meta['fw_hash'] = get_json_sem_hash(fw_map)
        self._meta['sw_hash'] = get_json_sem_hash(sw_map)
        ver = self._meta['version'].split('.')
        self._meta['major_version'] = int(ver[0])
        self._meta['minor_version'] = int(ver[1])
        self._meta['patch_version'] = int(ver[2])

    def resolve_all_data(self, data):
        """Resolve data info to provide a fully parsed config."""
        data = deepcopy(data)
        self.resolve_defines(data.get('defines', {}))
        self.resolve_metadata(data.get('metadata', {}))
        self.resolve_enumerations(data.get('enums', {}))
        self.resolve_bitfields(data.get('bitfields', {}))
        self.resolve_typedefs(data.get('typedefs', {}))
        self.resolve_maps(data.get('generated_maps', {}))
        self._resolve_overrides(data.get('overrides', {}))
        self._resolve_records_post()
        self._resolve_hashes()

    def get_cfg(self):
        """Get the full parsed configuration.

        This assumes that the input memory map data has already been resolved.
        """
        tds = []
        for td_name in self._tdo:
            tds.append({td_name: self.typedefs[td_name]})

        data_mapping = {
            'typedefs': tds,
            'bitfields': self._bfs,
            'enums': self._enums,
            'defines': self._defines,
            'metadata': self._meta,
        }
        data_mapping['maps'] = {}
        for mname, mval in self.maps.items():
            data_mapping['maps'][mname] = {
                'records': mval,
                'compressed_records': self._c_maps[mname],
                'type': self._maps_types[mname]
            }

        return data_mapping

    def _check_unique_types(self):
        tds = set(self.typedefs.keys())
        bfs = set(self._bfs.keys())
        enums = set(self._enums.keys())
        non_uni = tds.intersection(bfs)
        if non_uni:
            raise KeyError(f'Conflicting names ({non_uni}) '
                           'between bitfields and typedefs')
        non_uni = tds.intersection(enums)
        if non_uni:
            raise KeyError(f'Conflicting names ({non_uni}) '
                           'between enums and typedefs')
        non_uni = bfs.intersection(enums)
        if non_uni:
            raise KeyError(f'Conflicting names ({non_uni}) '
                           'between enums and bitfields')

    def _resolve_overrides(self, overrides):
        for record_name, data in overrides.items():
            found_match = False
            data['map'] = data.get('map', self._dflt_map)
            for record in self.maps[data['map']]:
                if record_name.startswith('r"') and record_name.endswith('"'):
                    reg_pattern = record_name[2:-1]
                    if not re.search(rf"{reg_pattern}", record['name']):
                        continue
                elif record['name'] != record_name:
                    continue
                new_rec = data.copy()
                del new_rec['map']
                new_rec['default_changed'] = False
                if new_rec.get('default', None) != record.get('default', None):
                    new_rec['default_changed'] = True

                record.update(new_rec)
                found_match = True
            if not found_match:
                raise KeyError(f'{record_name} '
                               'override did not match anything')

    def _rm_res_keys(self, typedef: dict) -> dict:
        inherit_prop = {}
        for key, val in typedef.items():
            if key not in self.RESERVED_KEYS:
                inherit_prop[key] = val

        return inherit_prop

    def _inherit_record(self, record: dict):
        all_props = {}
        for ovr in self._rec_parent_fields:
            all_props.update(ovr)
        all_props.update(record)
        return all_props

    def resolve_maps(self, maps):
        """Calculate offsets of records for map data."""
        if not maps:
            raise KeyError("At least 1 generated map is required")
        for mname, mmap in maps.items():
            self._map_offset = 0
            self._cur_map = mname
            self.maps[mname] = []
            self._c_maps[mname] = []
            first_type = self.typedefs[mmap['type']]
            self._maps_types[mname] = mmap['type']
            # Add default values to the parent so it can propagate
            first_type['read_permission'] = first_type.get('read_permission',
                                                           0)
            first_type['write_permission'] = first_type.get('write_permission',
                                                            0)
            self._rec_parent_fields = [self._rm_res_keys(first_type)]
            for record in first_type['elements']:
                self._resolve_records(record)
            self._find_compress_changes(self._c_maps[mname])
        if self._dflt_map is not None:
            if self._dflt_map not in maps.keys():
                raise KeyError(f'default map {self._dflt_map} '
                               'not defined in maps')
        if len(maps) == 1:
            self._dflt_map = list(maps.keys())[0]

    def _arr_nest(self, record, td_dict):
        self._compress_array.append({'size': record['resolved_array_size'],
                                     'uid': self._compress_uid})
        self._compress_uid += 1
        for idx in range(record['resolved_array_size']):
            self._compress_array[-1]['idx'] = idx
            old_prefix = self._record_prefix
            name = f'{record["name"]}[{idx}]'
            if self._record_prefix:
                self._record_prefix = f'{self._record_prefix}.{name}'
            else:
                self._record_prefix = name
            for element in td_dict['elements']:
                self._resolve_records(element)
            self._record_prefix = old_prefix
        del self._compress_array[-1]

    def _single_nest(self, record, rtype):
        old_prefix = self._record_prefix
        name = f'{record["name"]}'
        if self._record_prefix:
            self._record_prefix = f'{self._record_prefix}.{name}'
        else:
            self._record_prefix = name
        for element in self.typedefs[rtype]['elements']:
            self._resolve_records(element)
        self._record_prefix = old_prefix

    def _arr_bf_(self, record):
        self._compress_array.append({'size': record['resolved_array_size'],
                                     'uid': self._compress_uid})
        self._compress_uid += 1
        for idx in range(record['resolved_array_size']):
            self._compress_array[-1]['idx'] = idx
            old_prefix = self._record_prefix
            name = f'{record["name"]}[{idx}]'
            if self._record_prefix:
                self._record_prefix = f'{self._record_prefix}.{name}'
            else:
                self._record_prefix = name
            self._bitfield_record(record)
            self._map_offset += record['resolved_type_size']
            self._record_prefix = old_prefix
        del self._compress_array[-1]

    def _single_bf(self, record):
        old_prefix = self._record_prefix
        name = f'{record["name"]}'
        if self._record_prefix:
            self._record_prefix = f'{self._record_prefix}.{name}'
        else:
            self._record_prefix = name
        self._bitfield_record(record)
        self._map_offset += record['resolved_type_size']
        self._record_prefix = old_prefix

    def _arr_prim(self, record):
        self._compress_array.append({'size': record['resolved_array_size'],
                                     'uid': self._compress_uid})
        self._compress_uid += 1
        for idx in range(record['resolved_array_size']):
            self._compress_array[-1]['idx'] = idx
            new_rec = record.copy()
            new_rec['name'] = f'{new_rec["name"]}[{idx}]'
            if self._record_prefix:
                new_rec['name'] = f'{self._record_prefix}.{new_rec["name"]}'
            new_rec['map_offset'] = self._map_offset
            self._map_offset += new_rec['resolved_type_size']
            self._add_rec(new_rec)
        del self._compress_array[-1]

    def _single_prim(self, record):
        new_rec = record.copy()
        if self._record_prefix:
            new_rec['name'] = f'{self._record_prefix}.{new_rec["name"]}'
        new_rec['map_offset'] = self._map_offset
        self._map_offset += new_rec['resolved_total_size']
        self._add_rec(new_rec)

    def _resolve_records(self, record) -> list:
        rtype = record['resolved_type']
        if rtype in self.typedefs.keys():
            td_dict = self.typedefs[rtype]
            self._rec_parent_fields.append(self._rm_res_keys(record))
            self._rec_parent_fields.append(self._rm_res_keys(td_dict))
            if 'resolved_array_size' in record:
                self._arr_nest(record, td_dict)
            else:
                self._single_nest(record, rtype)
            del self._rec_parent_fields[-1]
            del self._rec_parent_fields[-1]
        elif rtype in self._bfs.keys():
            bf_dict = self._bfs[rtype]
            self._rec_parent_fields.append(self._rm_res_keys(bf_dict))
            if 'resolved_array_size' in record:
                self._arr_bf_(record)
            else:
                self._single_bf(record)
            del self._rec_parent_fields[-1]
        elif rtype in self.PRIMARIES:
            record = self._inherit_record(record)
            if 'resolved_array_size' in record:
                self._arr_prim(record)
            else:
                self._single_prim(record)
        else:
            raise KeyError(f'{rtype} type for map {self._cur_map} '
                           'does not exist')

    def _try_res_perm(self, rec, permt):
        if not isinstance(rec[permt], list):
            rec[permt] = [rec[permt]]
        res_perm = 0
        for perm in rec[permt]:
            if perm is None:
                continue
            if isinstance(perm, str):
                try:
                    rpu = self._meta['resolved_permission_users']
                    res_perm |= rpu[perm]
                except KeyError as exc:
                    msg = f'permissions not recognized in {rec}'
                    raise KeyError(msg) from exc
            else:
                res_perm |= int(perm)
        if res_perm >= 0x10:
            msg = f'{permt} must be less than 4 bits in {rec}'
            raise ValueError(msg)
        return res_perm

    def _add_rec(self, rec):
        rperm = 'read_permission'
        wperm = 'write_permission'
        rec[f'resolved_{rperm}'] = self._try_res_perm(rec, rperm)
        rec[f'resolved_{wperm}'] = self._try_res_perm(rec, wperm)

        rec['readable'] = bool(rec[f'resolved_{rperm}'])
        rec['writable'] = bool(rec[f'resolved_{wperm}'])
        access = rec[f'resolved_{wperm}']
        access |= rec[f'resolved_{rperm}'] << 4
        rec['resolved_access'] = access

        self.maps[self._cur_map].append(rec)
        crec = rec.copy()
        if len(self._compress_array) > 0:
            if all(d['idx'] == 0 for d in self._compress_array):
                # Rename a[0].b[0] to a[n].b[m]
                crec['compressed_info'] = []
                crec['compressed_offset'] = f'{crec["map_offset"]}'
                for idx, val in enumerate(self._compress_array):
                    idx_name = chr(ord('n') - idx)
                    crec['name'] = crec['name'].replace('[0]',
                                                        f'[{idx_name}]',
                                                        1)
                    msg = f'+{val["size"]}*{idx_name}'
                    crec['compressed_offset'] += msg
                    tmp = val.copy()
                    tmp['idx_name'] = idx_name
                    del tmp['idx']
                    crec['compressed_info'].append(tmp)
                self._c_maps[self._cur_map].append(crec)
        else:
            crec['compressed_offset'] = f'{crec["map_offset"]}'
            self._c_maps[self._cur_map].append(crec)

    def _find_compress_changes(self, records):
        """Calculate when a new array starts and ends.

        This is used for generating opening and closing for loop generation.
        """
        old_uid = []
        keyci = 'compressed_info'
        for idx, rec in enumerate(records):
            if keyci not in rec:
                continue
            for info_idx, info in enumerate(rec[keyci]):
                info['start'] = False
                uid = info['uid']
                if info_idx >= len(old_uid):
                    old_uid.append(-1)
                old_uid.extend([-1] * info_idx)
                if old_uid[info_idx] != uid:
                    info['start'] = True
                    old_uid[info_idx] = uid

                info['end'] = False
                try:

                    if records[idx + 1][keyci][info_idx]['uid'] != uid:
                        info['end'] = True
                        del old_uid[-1]
                except (KeyError, IndexError):
                    info['end'] = True
                    del old_uid[-1]

    def _bitfield_record(self, bf_rec):

        bf_rec = self._bfs[bf_rec['resolved_type']]
        t_size = bf_rec['resolved_type_size']
        for bitfield in bf_rec['elements']:
            bitfield = self._inherit_record(bitfield)
            new_rec = bitfield.copy()
            # bitfields will always have a prefix because a map must start with
            # a type
            new_rec['name'] = f'{self._record_prefix}.{new_rec["name"]}'
            new_rec['map_offset'] = self._map_offset
            new_rec['resolved_type_size'] = t_size
            self._add_rec(new_rec)

    def resolve_defines(self, defines):
        """Resolve defines using the unsafe eval.

        Example:
            input = [
                {
                    'a': {'value': 1},
                    'b': {'value': 'a'},
                    'c': {'value': '"my_string"'}
                },
                {
                    'd': {'value': 'a + b - 2'}
                }
            ]

            self._defines = {
                'a': {'value': 1, 'resolved_value': 1},
                'b': {'value': 'a', 'resolved_value': 1},
                'c': {'value': '"my_string"', 'resolved_value': "my_string"},
                'd': {'value': 'a + b - 2', 'resolved_value': 0},
            }

            self.resolved_defines = {
                'a': 1,
                'b': 1,
                'c': 'my_string',
                'd': 0
            }
        """
        resolved_defs = self.resolved_defs
        self._defines = defines
        while True:
            def_count = len(resolved_defs)
            finished = True
            for key in sorted(defines):
                if not isinstance(defines[key], dict):
                    defines[key] = {'value': defines[key]}
                val = defines[key]['value']
                try:
                    if isinstance(val, str):
                        if (val[0] != "\"" or val[-1] != "\""):
                            val = eval(val, None, resolved_defs)

                    resolved_defs[key] = val
                    defines[key]['resolved_value'] = val
                except (ValueError, NameError, TypeError):
                    finished = False
                    self.logger.debug("Cannot resolved on this pass")

            if finished:
                break
            if def_count == len(resolved_defs):
                missing_deps = set(defines.keys()) - set(resolved_defs.keys())
                raise RecursionError(f'Cannot resolve {missing_deps} defines '
                                     'due to missing definition/circular '
                                     'dependency')

    def _calc_td_elements(self, td_name, tds):
        elements = tds[td_name]['elements']
        tds[td_name]['use_bitfields'] = False
        tds[td_name]['use_enums'] = False
        use_defines = False
        deps = []
        offset = 0
        pad = 0
        for idx, ele in enumerate(elements.copy()):
            # Handle default, with only a name provided
            if isinstance(ele, str):
                ele = {'name': ele}

            r_type = ele.get('type', self.default_type)
            multi = 1
            if 'array_size' in ele:
                use_defines |= self._eval_with_defs(ele, 'array_size')
                multi = ele['resolved_array_size']
            if r_type in self.PRIMARIES:
                t_size = self.PRIMARIES[r_type]
            elif r_type in self._bfs:
                t_size = self._bfs[r_type]['resolved_type_size']
                tds[td_name]['use_bitfields'] = True
            elif r_type in self._enums:
                t_size = self._enums[r_type]['resolved_type_size']
                tds[td_name]['use_enums'] = True
                etype = self._enums[r_type].copy()
                del etype['elements']
                etype.update(ele)
                ele = etype
                ele['enum'] = r_type
                r_type = self._enums[r_type]['resolved_type']
            else:
                t_size = tds[r_type]['resolved_total_size']
                deps.append(r_type)
            ele['resolved_total_size'] = t_size * multi
            ele['resolved_type_size'] = t_size
            ele['resolved_offset'] = offset
            ele['resolved_type'] = r_type
            offset += t_size * multi
            elements[idx+pad] = ele
            if self._align:
                pad_size = self._align - offset % self._align
                if offset % self._align != 0:
                    elements.insert(idx + pad + 1,
                                    self._get_padded_type(offset,
                                                          pad_size,
                                                          pad))
                    offset += pad_size
                    pad += 1
        tds[td_name]['use_defines'] = use_defines
        tds[td_name]['deps'] = sorted(list(set(deps)))
        return offset

    def resolve_typedefs(self, typedefs):
        """Resolve typedef dependencies and apply default data."""
        tds = typedefs
        self._resolve_reference(tds)
        self._tdo = self._resolve_typedef_order(tds)
        self.typedefs = tds
        for td_name in self._tdo:
            offset = self._calc_td_elements(td_name, tds)
            elements = tds[td_name]['elements']
            if 'total_size' in tds[td_name]:
                tot_size = tds[td_name]['total_size']
                if offset > tot_size:
                    raise ValueError(f'{td_name} total size limit ({tot_size})'
                                     f' exceeds calculated size {offset}')
                if offset < tot_size:
                    pad_size = tot_size - offset
                    elements.append(self._get_padded_type(offset, pad_size))
                tds[td_name]['resolved_total_size'] = tot_size
            elif self._struct_align:
                pad_size = self._struct_align - offset % self._struct_align
                if offset % self._struct_align != 0:
                    elements.append(self._get_padded_type(offset, pad_size))
                tds[td_name]['resolved_total_size'] = offset + pad_size
            else:
                tds[td_name]['resolved_total_size'] = offset
            self._assert_unique_elements(elements, td_name)
        self._check_unique_types()

    def _get_padded_type(self, offset: int, size: int, name=None) -> dict:
        if name is not None:
            name = f'padding_{name}'
        else:
            name = 'padding'
        return {
            'name': name,
            'description': 'padding bytes',
            'reserved': True,
            'resolved_array_size': size,
            'resolved_offset': offset,
            'resolved_type_size': 1,
            'resolved_type': 'uint8_t',
            'resolved_total_size': size
        }

    def _resolve_typedef_order(self, typedefs):
        """Resolve the inherit property of the typedefs."""
        known_types = list(self.PRIMARIES.keys())
        kbfe = list(self._bfs.keys())
        kbfe.extend(self._enums.keys())
        unresolved_types = []
        while True:
            type_count = len(known_types)
            finished = True
            for td_name in sorted(typedefs.keys()):
                if td_name not in known_types:
                    for ele in typedefs[td_name]['elements']:
                        if isinstance(ele, str):
                            ele = {'name': ele}
                        r_type = ele.get('type', self.default_type)
                        if r_type not in known_types and r_type not in kbfe:
                            finished = False
                            unresolved_types.append(r_type)
                            break
                    else:
                        known_types.append(td_name)
                        if td_name in unresolved_types:
                            unresolved_types.remove(td_name)

            if finished:
                break
            if type_count == len(known_types):
                unresolved_types = list(set(unresolved_types))
                missing_deps = list(set(typedefs.keys()) - set(known_types))
                raise RecursionError(f'Cannot resolve {missing_deps} typedefs '
                                     'due to missing definition/circular '
                                     f'dependency/typo. {unresolved_types} '
                                     'types are not resolved.')
        return [x for x in known_types if x not in self.PRIMARIES]

    def _calc_rtype(self, bit_total, r_type):
        if r_type is None:
            if bit_total > 32:
                return 'uint64_t'
            if bit_total > 16:
                return 'uint32_t'
            if bit_total > 8:
                return 'uint16_t'
            return 'uint8_t'
        return r_type

    def resolve_bitfields(self, bitfields):
        """Resolve bitfields and apply default data."""
        bfs = bitfields
        self._resolve_reference(bfs)
        self._bfs = bfs
        for bf_key in sorted(bfs.keys()):
            r_type = bfs[bf_key].get('type', None)
            elements = bfs[bf_key]['elements']
            bit_total = 0
            for idx, ele in enumerate(elements):
                if isinstance(ele, str):
                    ele = {'name': ele}
                r_bit = eval(str(ele.get('bits', 1)), None, self.resolved_defs)
                if r_bit == 0:
                    raise ValueError(f'{ele["name"]} has 0 bits... tisk tisk')
                ele['resolved_bit_offset'] = bit_total
                bit_total += r_bit
                ele['resolved_bits'] = r_bit
                elements[idx] = ele
            if bit_total > 64:
                raise ValueError(f'Too many bits in {bf_key}, {bit_total}')

            bfs[bf_key]['resolved_type'] = self._calc_rtype(bit_total, r_type)
            r_size = self.PRIMARIES[bfs[bf_key]['resolved_type']]
            pad_bits = (r_size * 8) - bit_total
            if pad_bits < 0:
                raise ValueError(f'Too many bits ({pad_bits}) for {r_type}')
            if pad_bits > 0:
                elements.append(self._get_padded_bitfield(bit_total, pad_bits))
            bfs[bf_key]['resolved_type_size'] = r_size
            self._assert_unique_elements(elements, bf_key)

    def _get_padded_bitfield(self, offset, bits):
        return {
            'name': 'padding',
            'description': 'padding bits',
            'reserved': True,
            'resolved_bit_offset': offset,
            'resolved_bits': bits
        }

    def _bound_prim_size(self, prim_type: str, val: int):
        min_val = 0
        max_val = 0
        if prim_type.startswith('u'):
            max_val = (2 ** (8 * self.PRIMARIES[prim_type])) - 1
        elif prim_type.startswith('i'):
            max_val = (2 ** (8 * self.PRIMARIES[prim_type] - 1)) - 1
            min_val = -max_val - 1
        else:
            raise KeyError(f'{prim_type} not a valid type')
        if val < min_val or val > max_val:
            raise ValueError(f'{val} is out of bounds of {prim_type}')

    def resolve_enumerations(self, enums):
        """Resolve enumerations and apply default data."""
        self._resolve_reference(enums)
        self._enums = enums
        for enu_key in sorted(enums.keys()):
            enu = enums[enu_key]
            bitenum = enu.get('bitwise', False)
            prev_val = None
            elements = enu['elements']
            enu['resolved_type'] = enu.get("type", self.default_type)
            enu['resolved_type_size'] = self.PRIMARIES[enu['resolved_type']]
            use_defines = True
            for idx, ele in enumerate(elements):
                if isinstance(ele, str):
                    ele = {'name': ele}

                if 'value' not in ele:
                    if bitenum:
                        if prev_val is None:
                            ele['resolved_value'] = 1
                        else:
                            # pylint: disable-next=unsubscriptable-object
                            bit = prev_val['resolved_value'].bit_length()
                            bit = 1 << (bit)
                            ele['resolved_value'] = bit
                    else:
                        if prev_val is None:
                            ele['resolved_value'] = 0
                        else:
                            # pylint: disable-next=unsubscriptable-object
                            ele['resolved_value'] = prev_val['resolved_value']
                            ele['resolved_value'] += 1
                else:
                    use_defines |= self._eval_with_defs(ele, 'value')
                try:
                    self._bound_prim_size(enu['resolved_type'],
                                          ele['resolved_value'])
                except (ValueError, KeyError) as exc:
                    raise ValueError(f'{enu_key} parsing error') from exc

                elements[idx] = ele
                prev_val = ele
            enu['use_defines'] = use_defines
            self._assert_unique_elements(elements, enu_key)

    def resolve_metadata(self, metadatas):
        """Resolve metadata filling in missing data."""
        mds = metadatas

        # We should exit only because if a test overrides the _struct_align or
        # _align it will go back to 0
        if len(mds) == 0:
            return
        self._align = mds.get('align', None)
        self._struct_align = mds.get('struct_align', None)
        self._dflt_map = mds.get('default_map', None)
        self.default_type = mds.get('default_type', self._DEFAULT_TYPE)
        mds['version'] = mds.get('version', '0.0.0')
        mds['resolved_permission_users'] = {}
        for idx, user in enumerate(mds.get('permission_users', [])):
            mds['resolved_permission_users'][user] = 1 << (idx)
        self._meta = mds

    def _resolve_reference(self, dicts_with_elements):
        dwe = dicts_with_elements
        resolved_refs = []
        unresolved_regs = []
        while True:
            resolved_refs_count = len(resolved_refs)
            finished = True
            for key in sorted(dwe):
                if 'reference' in dwe[key]:
                    ref_key = dwe[key]['reference']
                    ele = 'elements'
                    # inserts all elements from the reference entry to the
                    # the start
                    dwe[key][ele] = dwe[ref_key][ele] + dwe[key][ele]
                    # If the referenced entry contains another entry we need
                    # to propagate it
                    if 'reference' in dwe[ref_key]:
                        dwe[key]['reference'] = dwe[ref_key]['reference']
                        finished = False
                        unresolved_regs.append(key)
                    else:
                        dwe[key].pop('reference')
                        resolved_refs.append(key)

            if finished:
                break
            if resolved_refs_count == len(resolved_refs):
                missing_deps = set(unresolved_regs) - set(resolved_refs)
                raise RecursionError(f'Cannot resolve {missing_deps} '
                                     'references due to circular dependency')

    def _assert_unique_elements(self, elements, key):
        names = []
        for ele in elements:
            name = ele['name']
            if name in names:
                raise KeyError(f'Duplicate record {name} in {key}')
            names.append(name)

    def _resolve_records_post(self):
        for records in self.maps.values():
            for rec in records:
                self._resolve_record_props(rec)

    def _resolve_record_props(self, rec):
        self._eval_with_defs(rec, 'scaling_factor')
        self._eval_and_apply_scaling(rec, 'default')
        self._eval_and_apply_scaling(rec, 'min')
        self._eval_and_apply_scaling(rec, 'max')

    def _eval_with_defs(self, rec, key):
        if key not in rec:
            return False
        rec[f'resolved_{key}'] = eval(str(rec[key]), None, self.resolved_defs)
        if rec[key] != rec[f'resolved_{key}']:
            return True
        return False

    def _eval_and_apply_scaling(self, rec, key):
        if key not in rec:
            return
        self._eval_with_defs(rec, key)
        if 'resolved_scaling_factor' not in rec:
            return
        val = rec[f'resolved_{key}']
        val /= rec['resolved_scaling_factor']
        rec[f'resolved_scaled_{key}'] = val
        if self._rec_needs_casting(rec):
            rec[f'resolved_scaled_{key}'] = int(val)

    def _rec_needs_casting(self, rec):
        if 'int' in rec.get('resolved_type', ''):
            return True
        if 'resolved_bits' in rec:
            return True
        return False
