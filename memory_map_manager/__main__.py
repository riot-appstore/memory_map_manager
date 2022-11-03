#!/usr/bin/env python3
# coding=utf-8
# Copyright (c) 2022 Kevin Weiss, for HAW Hamburg  <kevin.weiss@haw-hamburg.de>
#
# This file is subject to the terms and conditions of the MIT License. See the
# file LICENSE in the top level directory for more details.
# SPDX-License-Identifier:    MIT
"""The application that generates the code."""
import argparse
import glob
import logging
from os import path, makedirs, remove

from memory_map_manager import MMMImporter, MMMExporter, MMMConfigParser


def _write_files(files: dict, fdir, clean, exts):
    if not path.exists(fdir):
        makedirs(fdir)
    elif clean:
        for ext in exts:
            for filename in glob.glob(path.join(fdir, f'mm_*.{ext}')):
                logging.info("Removing %r", filename)
                remove(filename)
    for fname, fdata in files.items():
        fpath = path.join(fdir, fname)
        logging.info("Creating %r", fpath)
        with open(fpath, 'w', encoding="utf-8") as fhandle:
            fhandle.write(fdata)


def main():
    """Parse typedefs and create outputs."""
    log_levels = ('debug', 'info', 'warning', 'error', 'fatal', 'critical')

    parser = argparse.ArgumentParser()

    parser.add_argument("--cfg-path", "-p",
                        help='the path to the memory map manager '
                             'configuration importer.',
                        default='main.yaml')

    parser.add_argument("--clean", "-C", action="store_true",
                        help='clean the generated directories before '
                             'generation. Be careful!')

    parser.add_argument('--loglevel', choices=log_levels, default='info',
                        help='python logger log level, defaults to "info"')
    args = parser.parse_args()
    loglevel = logging.getLevelName(args.loglevel.upper())
    logging.basicConfig(level=loglevel)
    logging.info("Starting memory_map_manager")

    logging.info("Using %r for importer", args.cfg_path)
    importer = MMMImporter(args.cfg_path)

    parser = MMMConfigParser(importer.mm_data)
    exporter = MMMExporter(parser.get_cfg(), importer.mm_data)
    if importer.c_dir:
        _write_files(exporter.gen_c_files(), importer.c_dir,
                     args.clean, ['c', 'h'])
    if importer.csv_dir:
        _write_files(exporter.gen_csv_files(), importer.csv_dir,
                     args.clean, ['csv'])
    if importer.cfg_dir:
        _write_files(exporter.gen_cfg_files(), importer.cfg_dir,
                     args.clean, ['yaml'])
    if not importer.c_dir and not importer.csv_dir and not importer.cfg_dir:
        logging.warning("No directories to output specified")
    else:
        print("SUCCESS")


if __name__ == "__main__":  # pragma: no cover
    main()
