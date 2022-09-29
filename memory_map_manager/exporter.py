# coding=utf-8
# Copyright (c) 2022 Kevin Weiss, for HAW Hamburg  <kevin.weiss@haw-hamburg.de>
#
# This file is subject to the terms and conditions of the MIT License. See the
# file LICENSE in the top level directory for more details.
# SPDX-License-Identifier:    MIT
"""Exports generated code to csv, c, and configurations."""
import csv
from io import StringIO
import json
import logging

from jinja2 import Environment, PackageLoader, select_autoescape
from yaml import safe_dump

from ._version import __version__ as MMM_VERSION


class MMMExporter():
    """Memory map manager exporter.

    Generates output strings based on parsed input configurations.
    """

    def __init__(self, mm_cfg, mm_input_data=None,
                 hide_version=False, line_width=80):
        """Instantiate the exporter with input data and jinja env."""
        self.logger = logging.getLogger(self.__class__.__name__)
        self._cfg = mm_cfg
        self._mm_input_data = mm_input_data
        meta = self._cfg['metadata']

        self._jenv = Environment(loader=PackageLoader("memory_map_manager"),
                                 autoescape=select_autoescape())
        self._jargs = {'line_width': line_width,
                       'if_version': meta.get('version', 'unknown'),
                       'mmm_version': MMM_VERSION,
                       'hide_version': hide_version}

    def _gen_access_map_c(self) -> dict:
        files = {}
        if not self._cfg['metadata']['resolved_permission_users']:
            return files
        tmpl = self._jenv.get_template("mm_access_map.c.j2")
        for map_name, mdata in self._cfg['maps'].items():
            mdata = mdata['records']
            fname = f'mm_access_{map_name.lower()}.c'
            files[fname] = tmpl.render(filename=fname,
                                       map_name=map_name,
                                       is_header_file=False,
                                       records=mdata,
                                       **self._jargs)
        return files

    def _gen_access_map_h(self) -> dict:
        files = {}
        if not self._cfg['metadata']['resolved_permission_users']:
            return files
        tmpl = self._jenv.get_template("mm_access_map.h.j2")
        for map_name in self._cfg['maps']:
            fname = f'mm_access_{map_name.lower()}.h'
            files[fname] = tmpl.render(filename=fname,
                                       map_name=map_name,
                                       is_header_file=True,
                                       **self._jargs)
        return files

    def _gen_access_types_h(self) -> dict:
        files = {}
        if not self._cfg['metadata']['resolved_permission_users']:
            return files
        tmpl = self._jenv.get_template("mm_access_types.h.j2")
        # Since python 3.7, the insertion order of dicts are preserved
        # thus we do not need to sort the lowest number first... yay.
        rup = self._cfg['metadata']['resolved_permission_users']
        fname = 'mm_access_types.h'
        files[fname] = tmpl.render(filename=fname,
                                   is_header_file=True,
                                   permission_users=rup,
                                   **self._jargs)
        return files

    def _gen_access_h(self) -> dict:
        files = {}
        if not self._cfg['metadata']['resolved_permission_users']:
            return files
        tmpl = self._jenv.get_template("mm_access.h.j2")
        fname = 'mm_access.h'
        files[fname] = tmpl.render(filename=fname,
                                   map_names=self._cfg['maps'].keys(),
                                   is_header_file=True,
                                   **self._jargs)
        return files

    def _gen_default_map_c(self) -> dict:
        files = {}
        tmpl = self._jenv.get_template("mm_default_map.c.j2")
        for map_name, mdata in self._cfg['maps'].items():
            resd = 'resolved_default'
            usedef = any(rec.get('use_defines') for rec in mdata['records'])
            if not any(resd in rec for rec in mdata['records']):
                continue
            fname = f'mm_default_{map_name.lower()}.c'
            files[fname] = tmpl.render(filename=fname,
                                       map_name=map_name,
                                       use_defines=usedef,
                                       is_header_file=False,
                                       map_data=mdata,
                                       **self._jargs)
        return files

    def _gen_default_map_h(self) -> dict:
        files = {}
        tmpl = self._jenv.get_template("mm_default_map.h.j2")
        for map_name, mdata in self._cfg['maps'].items():
            resd = 'resolved_default'
            usedef = any(rec.get('use_defines') for rec in mdata['records'])
            if not any(resd in rec for rec in mdata['records']):
                continue
            fname = f'mm_default_{map_name.lower()}.h'
            files[fname] = tmpl.render(filename=fname,
                                       map_name=map_name,
                                       use_defines=usedef,
                                       is_header_file=True,
                                       map_data=mdata,
                                       **self._jargs)
        return files

    def _gen_defs_h(self) -> dict:
        files = {}
        if not self._cfg['defines']:
            return files
        tmpl = self._jenv.get_template("mm_defs.h.j2")
        fname = 'mm_defs.h'
        files[fname] = tmpl.render(filename=fname,
                                   map_name='defs',
                                   is_header_file=True,
                                   defs=self._cfg['defines'],
                                   **self._jargs)
        return files

    def _gen_bitfields_h(self) -> dict:
        files = {}
        if not self._cfg['bitfields']:
            return files
        tmpl = self._jenv.get_template("mm_bitfields.h.j2")
        fname = 'mm_bitfields.h'
        files[fname] = tmpl.render(filename=fname,
                                   map_name='bitfields',
                                   is_header_file=True,
                                   has_defs=bool(self._cfg['defines']),
                                   bitfields=self._cfg['bitfields'],
                                   **self._jargs)
        return files

    def _gen_typedef_type_h(self) -> dict:
        files = {}
        tmpl = self._jenv.get_template("mm_typedefs_type.h.j2")
        for tpd in self._cfg['typedefs']:
            name = next(iter(tpd))
            fname = f'mm_typedefs_{name}.h'
            files[fname] = tmpl.render(filename=fname,
                                       map_name='typedefs',
                                       is_header_file=True,
                                       typedef=tpd[name],
                                       name=name,
                                       **self._jargs)
        return files

    def _gen_typedef_map_h(self) -> dict:
        files = {}
        tmpl = self._jenv.get_template("mm_typedefs_map.h.j2")
        for map_name, mdata in self._cfg['maps'].items():
            fname = f'mm_typedefs_{map_name}.h'
            typedef = None
            for tpd in self._cfg['typedefs']:
                name = next(iter(tpd))
                if name == mdata['type']:
                    typedef = tpd[name]
            typedef['deps'].append(mdata['type'])

            files[fname] = tmpl.render(filename=fname,
                                       map_name=map_name,
                                       is_header_file=True,
                                       name=name,
                                       typedef=typedef,
                                       **self._jargs)
        return files

    def _gen_typedef_h(self) -> dict:
        files = {}
        tmpl = self._jenv.get_template("mm_typedefs.h.j2")
        fname = 'mm_typedefs.h'
        files[fname] = tmpl.render(filename=fname,
                                   map_name='typedef',
                                   map_names=self._cfg['maps'].keys(),
                                   is_header_file=True,
                                   **self._jargs)
        return files

    def _gen_cc_h(self) -> dict:
        files = {}
        tmpl = self._jenv.get_template("mm_cc.h.j2")
        fname = 'mm_cc.h'
        files[fname] = tmpl.render(filename=fname,
                                   map_name='cc',
                                   is_header_file=True,
                                   **self._jargs)
        return files

    def _gen_meta_h(self) -> dict:
        files = {}
        tmpl = self._jenv.get_template("mm_meta.h.j2")
        fname = 'mm_meta.h'
        files[fname] = tmpl.render(filename=fname,
                                   map_name='meta',
                                   meta=self._cfg['metadata'],
                                   is_header_file=True,
                                   **self._jargs)
        return files

    def _gen_enums_h(self) -> dict:
        files = {}
        if not self._cfg['enums']:
            return files
        tmpl = self._jenv.get_template("mm_enums.h.j2")
        fname = 'mm_enums.h'
        files[fname] = tmpl.render(filename=fname,
                                   map_name='enums',
                                   enums=self._cfg['enums'],
                                   is_header_file=True,
                                   **self._jargs)
        return files

    def _gen_legacy_csv(self) -> dict:
        files = {}
        version = self._cfg['metadata']['version']
        app_name = self._cfg['metadata']['app_name']
        for map_name, mdata in self._cfg['maps'].items():
            fname = f'mm_{app_name}_{map_name}_{version.replace(".", "_")}.csv'
            output = StringIO()
            fieldnames = ['name',
                          'offset',
                          'total_size',
                          'type_size',
                          'type',
                          'description',
                          'access',
                          'array_size',
                          'bit_offset',
                          'bits',
                          'default',
                          'flag',
                          'max',
                          'min'
                          ]
            writer = csv.DictWriter(output, extrasaction='ignore',
                                    fieldnames=fieldnames)
            writer.writeheader()
            for record in mdata['records']:
                record = record.copy()
                record['offset'] = record.get('map_offset', None)
                record['total_size'] = record.get('resolved_total_size', None)
                record['type_size'] = record.get('resolved_type_size', None)
                record['array_size'] = record.get('resolved_array_size', None)
                record['bit_offset'] = record.get('resolved_bit_offset', None)
                record['bits'] = record.get('resolved_bits', None)
                record['access'] = record.get('resolved_access', None)
                if record['array_size']:
                    if record['name'].endswith('[0]'):
                        record['name'] = record['name'][:-3]
                        writer.writerow(record)
                else:
                    writer.writerow(record)
            files[fname] = output.getvalue()
        return files

    def _get_unique_fields(self, records, user=None):
        fieldnames = set()
        for rec in records:
            # If we have read permission then we want to add it.
            if user is None or (user & rec['resolved_access']):
                fieldnames.update(rec.keys())
        return sorted(list(fieldnames))

    def _gen_full_csv(self) -> dict:
        files = {}
        meta = self._cfg['metadata']
        app_name = meta['app_name']
        for map_name, mdata in self._cfg['maps'].items():
            fname = f'mm_{app_name}_{map_name}_{meta["full_hash"]}.csv'
            output = StringIO()
            fieldnames = self._get_unique_fields(mdata['records'])
            writer = csv.DictWriter(output, extrasaction='ignore',
                                    fieldnames=fieldnames)
            writer.writeheader()
            for record in mdata['records']:
                writer.writerow(record)
            files[fname] = output.getvalue()
        return files

    def _gen_user_csv(self) -> dict:
        files = {}
        meta = self._cfg['metadata']
        app_name = meta['app_name']
        for idx, user in enumerate(meta.get('permission_users', [])):
            for map_name, mdata in self._cfg['maps'].items():
                mhash = meta["full_hash"]
                fname = f'mm_{app_name}_{map_name}_{user}_{mhash}.csv'
                output = StringIO()
                # only look at the read_permission access
                fieldnames = self._get_unique_fields(mdata['records'],
                                                     0x10 << idx)
                writer = csv.DictWriter(output, extrasaction='ignore',
                                        fieldnames=fieldnames)
                writer.writeheader()
                has_data = False
                for record in mdata['compressed_records']:
                    if (0x10 << idx) & record['resolved_access']:
                        has_data = True
                        writer.writerow(record)
                if has_data:
                    files[fname] = output.getvalue()
        return files

    def _gen_compressed_csv(self) -> dict:
        files = {}
        version = self._cfg['metadata']['version']
        app_name = self._cfg['metadata']['app_name']
        for map_name, mdata in self._cfg['maps'].items():
            ver = version.replace(".", "_")
            fname = f'mm_{app_name}_{map_name}_compressed_{ver}.csv'
            output = StringIO()
            crs = mdata['compressed_records']
            all_names = list(sorted(set().union(*(rec.keys() for rec in crs))))
            fieldnames = ['name',
                          'compressed_offset',
                          'resolved_total_size',
                          'resolved_type_size',
                          'resolved_type',
                          'description']
            for name in all_names:
                if name not in fieldnames:
                    fieldnames.append(name)

            writer = csv.DictWriter(output, extrasaction='ignore',
                                    fieldnames=fieldnames)
            writer.writeheader()
            for record in mdata['compressed_records'].copy():
                writer.writerow(record)
            files[fname] = output.getvalue()
        return files

    def _gen_cfg(self) -> str:
        meta = self._cfg['metadata']
        return {f'mm_{meta["full_hash"]}_cfg.json': json.dumps(self._cfg,
                                                               sort_keys=True,
                                                               indent=2)}

    def _gen_input_cfg(self) -> str:
        return {'mm_input_cfg.yaml': safe_dump(self._mm_input_data,
                                               indent=2, sort_keys=True)}

    def gen_c_files(self) -> dict:
        """Create c file strings based on configuration.

        Returns:
            dict[str]: A dictionary where the keys are the filenames and the
                       values are the file contents.
        """
        files = {}
        files.update(self._gen_access_h())
        files.update(self._gen_access_map_c())
        files.update(self._gen_access_map_h())
        files.update(self._gen_access_types_h())
        files.update(self._gen_bitfields_h())
        files.update(self._gen_default_map_c())
        files.update(self._gen_default_map_h())
        files.update(self._gen_defs_h())
        files.update(self._gen_typedef_h())
        files.update(self._gen_typedef_type_h())
        files.update(self._gen_typedef_map_h())
        files.update(self._gen_cc_h())
        files.update(self._gen_meta_h())
        files.update(self._gen_enums_h())
        return files

    def gen_csv_files(self) -> dict:
        """Create csv file strings based on configuration.

        Returns:
            dict[str]: A dictionary where the keys are the filenames and the
                       values are the file contents.
        """
        files = {}
        files.update(self._gen_full_csv())
        files.update(self._gen_legacy_csv())
        files.update(self._gen_compressed_csv())
        files.update(self._gen_user_csv())
        return files

    def gen_cfg_files(self) -> dict:
        """Create configuration file strings based on configuration.

        Returns:
            dict[str]: A dictionary where the keys are the filenames and the
                       values are the file contents.
        """
        files = {}
        files.update(self._gen_cfg())
        if self._mm_input_data:
            files.update(self._gen_input_cfg())
        return files
