# Copyright (c) 2018 Kevin Weiss, for HAW Hamburg  <kevin.weiss@haw-hamburg.de>
#
# This file is subject to the terms and conditions of the MIT License. See the
# file LICENSE in the top level directory for more details.
# SPDX-License-Identifier:    MIT
"""Tests Serial Driver implmentation in RIOT PAL."""
import pytest
import json
from memory_map_manager import MMMExporter

@pytest.fixture
def map_simple_full():
    json_cfg = """{
  "bitfields": {
    "bf_1": {
      "elements": [
        {
          "name": "field_1",
          "resolved_bit_offset": 0,
          "resolved_bits": 1
        },
        {
          "name": "field_2",
          "resolved_bit_offset": 1,
          "resolved_bits": 1
        },
        {
          "description": "padding bits",
          "name": "padding",
          "reserved": true,
          "resolved_bit_offset": 2,
          "resolved_bits": 6
        }
      ],
      "resolved_type": "uint8_t",
      "resolved_type_size": 1
    },
    "bf_2": {
      "elements": [
        {
          "bits": 12,
          "name": "field_1",
          "resolved_bit_offset": 0,
          "resolved_bits": 12
        },
        {
          "description": "padding bits",
          "name": "padding",
          "reserved": true,
          "resolved_bit_offset": 12,
          "resolved_bits": 4
        }
      ],
      "resolved_type": "uint16_t",
      "resolved_type_size": 2
    }
  },
  "defines": {
    "def_1": {
      "resolved_value": 3,
      "value": 3
    }
  },
  "enums": {
    "enum_1": {
      "elements": [
        {
          "name": "opt_1",
          "resolved_value": 0
        },
        {
          "name": "opt_2",
          "resolved_value": 1
        }
      ],
      "resolved_type": "uint32_t",
      "resolved_type_size": 4,
      "use_defines": true
    }
  },
  "maps": {
    "map_1": {
      "compressed_records": [
        {
          "compressed_offset": "0",
          "default": 1,
          "map_offset": 0,
          "name": "record_1",
          "read_permission": [
            "user"
          ],
          "readable": true,
          "resolved_access": 17,
          "resolved_offset": 0,
          "resolved_read_permission": 1,
          "resolved_total_size": 4,
          "resolved_type": "uint32_t",
          "resolved_type_size": 4,
          "resolved_write_permission": 1,
          "type": "uint32_t",
          "use_bitfields": true,
          "use_defines": true,
          "use_enums": false,
          "writable": true,
          "write_permission": [
            "user"
          ]
        },
        {
          "array_size": 2,
          "compressed_info": [
            {
              "end": true,
              "idx_name": "n",
              "size": 2,
              "start": true,
              "uid": 1
            }
          ],
          "compressed_offset": "4+2*n",
          "default": 2,
          "map_offset": 4,
          "name": "record_2[n]",
          "read_permission": [
            "user"
          ],
          "readable": true,
          "resolved_access": 16,
          "resolved_array_size": 2,
          "resolved_offset": 4,
          "resolved_read_permission": 1,
          "resolved_total_size": 4,
          "resolved_type": "uint16_t",
          "resolved_type_size": 2,
          "resolved_write_permission": 0,
          "type": "uint16_t",
          "use_bitfields": true,
          "use_defines": true,
          "use_enums": false,
          "writable": false,
          "write_permission": [
            0
          ]
        },
        {
          "array_size": "def_1",
          "compressed_info": [
            {
              "end": true,
              "idx_name": "n",
              "size": 3,
              "start": true,
              "uid": 2
            }
          ],
          "compressed_offset": "8+3*n",
          "default": "def_1",
          "map_offset": 8,
          "name": "record_3[n]",
          "read_permission": [
            0
          ],
          "readable": false,
          "resolved_access": 1,
          "resolved_array_size": 3,
          "resolved_offset": 8,
          "resolved_read_permission": 0,
          "resolved_total_size": 3,
          "resolved_type": "uint8_t",
          "resolved_type_size": 1,
          "resolved_write_permission": 1,
          "type": "uint8_t",
          "use_bitfields": true,
          "use_defines": true,
          "use_enums": false,
          "writable": true,
          "write_permission": [
            "user"
          ]
        },
        {
          "compressed_offset": "11",
          "map_offset": 11,
          "name": "record_4.field_1",
          "read_permission": [
            0
          ],
          "readable": false,
          "resolved_access": 0,
          "resolved_bit_offset": 0,
          "resolved_bits": 1,
          "resolved_read_permission": 0,
          "resolved_type_size": 1,
          "resolved_write_permission": 0,
          "use_bitfields": true,
          "use_defines": true,
          "use_enums": false,
          "writable": false,
          "write_permission": [
            0
          ]
        },
        {
          "compressed_offset": "11",
          "map_offset": 11,
          "name": "record_4.field_2",
          "read_permission": [
            0
          ],
          "readable": false,
          "resolved_access": 0,
          "resolved_bit_offset": 1,
          "resolved_bits": 1,
          "resolved_read_permission": 0,
          "resolved_type_size": 1,
          "resolved_write_permission": 0,
          "use_bitfields": true,
          "use_defines": true,
          "use_enums": false,
          "writable": false,
          "write_permission": [
            0
          ]
        },
        {
          "compressed_offset": "11",
          "description": "padding bits",
          "map_offset": 11,
          "name": "record_4.padding",
          "read_permission": [
            0
          ],
          "readable": false,
          "reserved": true,
          "resolved_access": 0,
          "resolved_bit_offset": 2,
          "resolved_bits": 6,
          "resolved_read_permission": 0,
          "resolved_type_size": 1,
          "resolved_write_permission": 0,
          "use_bitfields": true,
          "use_defines": true,
          "use_enums": false,
          "writable": false,
          "write_permission": [
            0
          ]
        },
        {
          "compressed_info": [
            {
              "end": false,
              "idx_name": "n",
              "size": 1,
              "start": true,
              "uid": 3
            }
          ],
          "compressed_offset": "12+1*n",
          "map_offset": 12,
          "name": "record_5[n].field_1",
          "read_permission": [
            0
          ],
          "readable": false,
          "resolved_access": 0,
          "resolved_bit_offset": 0,
          "resolved_bits": 1,
          "resolved_read_permission": 0,
          "resolved_type_size": 1,
          "resolved_write_permission": 0,
          "use_bitfields": true,
          "use_defines": true,
          "use_enums": false,
          "writable": false,
          "write_permission": [
            0
          ]
        },
        {
          "compressed_info": [
            {
              "end": false,
              "idx_name": "n",
              "size": 1,
              "start": false,
              "uid": 3
            }
          ],
          "compressed_offset": "12+1*n",
          "map_offset": 12,
          "name": "record_5[n].field_2",
          "read_permission": [
            0
          ],
          "readable": false,
          "resolved_access": 0,
          "resolved_bit_offset": 1,
          "resolved_bits": 1,
          "resolved_read_permission": 0,
          "resolved_type_size": 1,
          "resolved_write_permission": 0,
          "use_bitfields": true,
          "use_defines": true,
          "use_enums": false,
          "writable": false,
          "write_permission": [
            0
          ]
        },
        {
          "compressed_info": [
            {
              "end": true,
              "idx_name": "n",
              "size": 1,
              "start": false,
              "uid": 3
            }
          ],
          "compressed_offset": "12+1*n",
          "description": "padding bits",
          "map_offset": 12,
          "name": "record_5[n].padding",
          "read_permission": [
            0
          ],
          "readable": false,
          "reserved": true,
          "resolved_access": 0,
          "resolved_bit_offset": 2,
          "resolved_bits": 6,
          "resolved_read_permission": 0,
          "resolved_type_size": 1,
          "resolved_write_permission": 0,
          "use_bitfields": true,
          "use_defines": true,
          "use_enums": false,
          "writable": false,
          "write_permission": [
            0
          ]
        },
        {
          "bits": 12,
          "compressed_info": [
            {
              "end": false,
              "idx_name": "n",
              "size": 3,
              "start": true,
              "uid": 4
            }
          ],
          "compressed_offset": "13+3*n",
          "map_offset": 13,
          "name": "record_6[n].field_1",
          "read_permission": [
            0
          ],
          "readable": false,
          "resolved_access": 0,
          "resolved_bit_offset": 0,
          "resolved_bits": 12,
          "resolved_read_permission": 0,
          "resolved_type_size": 2,
          "resolved_write_permission": 0,
          "use_bitfields": true,
          "use_defines": true,
          "use_enums": false,
          "writable": false,
          "write_permission": [
            0
          ]
        },
        {
          "compressed_info": [
            {
              "end": true,
              "idx_name": "n",
              "size": 3,
              "start": false,
              "uid": 4
            }
          ],
          "compressed_offset": "13+3*n",
          "description": "padding bits",
          "map_offset": 13,
          "name": "record_6[n].padding",
          "read_permission": [
            0
          ],
          "readable": false,
          "reserved": true,
          "resolved_access": 0,
          "resolved_bit_offset": 12,
          "resolved_bits": 4,
          "resolved_read_permission": 0,
          "resolved_type_size": 2,
          "resolved_write_permission": 0,
          "use_bitfields": true,
          "use_defines": true,
          "use_enums": false,
          "writable": false,
          "write_permission": [
            0
          ]
        },
        {
          "compressed_offset": "19",
          "map_offset": 19,
          "name": "record_7.record_1",
          "read_permission": [
            0
          ],
          "readable": false,
          "resolved_access": 0,
          "resolved_offset": 0,
          "resolved_read_permission": 0,
          "resolved_total_size": 4,
          "resolved_type": "uint32_t",
          "resolved_type_size": 4,
          "resolved_write_permission": 0,
          "use_bitfields": false,
          "use_defines": false,
          "use_enums": false,
          "writable": false,
          "write_permission": [
            0
          ]
        },
        {
          "compressed_info": [
            {
              "end": true,
              "idx_name": "n",
              "size": 4,
              "start": true,
              "uid": 5
            }
          ],
          "compressed_offset": "23+4*n",
          "map_offset": 23,
          "name": "record_8[n].record_1",
          "read_permission": [
            0
          ],
          "readable": false,
          "resolved_access": 0,
          "resolved_offset": 0,
          "resolved_read_permission": 0,
          "resolved_total_size": 4,
          "resolved_type": "uint32_t",
          "resolved_type_size": 4,
          "resolved_write_permission": 0,
          "use_bitfields": false,
          "use_defines": false,
          "use_enums": false,
          "writable": false,
          "write_permission": [
            0
          ]
        },
        {
          "compressed_info": [
            {
              "end": true,
              "idx_name": "n",
              "size": 3,
              "start": true,
              "uid": 6
            }
          ],
          "compressed_offset": "39+3*n",
          "map_offset": 39,
          "name": "record_9[n].record_1",
          "read_permission": [
            0
          ],
          "readable": false,
          "resolved_access": 0,
          "resolved_offset": 0,
          "resolved_read_permission": 0,
          "resolved_total_size": 4,
          "resolved_type": "uint32_t",
          "resolved_type_size": 4,
          "resolved_write_permission": 0,
          "use_bitfields": false,
          "use_defines": false,
          "use_enums": false,
          "writable": false,
          "write_permission": [
            0
          ]
        }
      ],
      "records": [
        {
          "default": 1,
          "map_offset": 0,
          "name": "record_1",
          "read_permission": [
            "user"
          ],
          "readable": true,
          "resolved_access": 17,
          "resolved_default": 1,
          "resolved_offset": 0,
          "resolved_read_permission": 1,
          "resolved_total_size": 4,
          "resolved_type": "uint32_t",
          "resolved_type_size": 4,
          "resolved_write_permission": 1,
          "type": "uint32_t",
          "use_bitfields": true,
          "use_defines": true,
          "use_enums": false,
          "writable": true,
          "write_permission": [
            "user"
          ]
        },
        {
          "array_size": 2,
          "default": 2,
          "map_offset": 4,
          "name": "record_2[0]",
          "read_permission": [
            "user"
          ],
          "readable": true,
          "resolved_access": 16,
          "resolved_array_size": 2,
          "resolved_default": 2,
          "resolved_offset": 4,
          "resolved_read_permission": 1,
          "resolved_total_size": 4,
          "resolved_type": "uint16_t",
          "resolved_type_size": 2,
          "resolved_write_permission": 0,
          "type": "uint16_t",
          "use_bitfields": true,
          "use_defines": true,
          "use_enums": false,
          "writable": false,
          "write_permission": [
            0
          ]
        },
        {
          "array_size": 2,
          "default": 2,
          "map_offset": 6,
          "name": "record_2[1]",
          "read_permission": [
            "user"
          ],
          "readable": true,
          "resolved_access": 16,
          "resolved_array_size": 2,
          "resolved_default": 2,
          "resolved_offset": 4,
          "resolved_read_permission": 1,
          "resolved_total_size": 4,
          "resolved_type": "uint16_t",
          "resolved_type_size": 2,
          "resolved_write_permission": 0,
          "type": "uint16_t",
          "use_bitfields": true,
          "use_defines": true,
          "use_enums": false,
          "writable": false,
          "write_permission": [
            0
          ]
        },
        {
          "array_size": "def_1",
          "default": "def_1",
          "map_offset": 8,
          "name": "record_3[0]",
          "read_permission": [
            0
          ],
          "readable": false,
          "resolved_access": 1,
          "resolved_array_size": 3,
          "resolved_default": 3,
          "resolved_offset": 8,
          "resolved_read_permission": 0,
          "resolved_total_size": 3,
          "resolved_type": "uint8_t",
          "resolved_type_size": 1,
          "resolved_write_permission": 1,
          "type": "uint8_t",
          "use_bitfields": true,
          "use_defines": true,
          "use_enums": false,
          "writable": true,
          "write_permission": [
            "user"
          ]
        },
        {
          "array_size": "def_1",
          "default": "def_1",
          "map_offset": 9,
          "name": "record_3[1]",
          "read_permission": [
            0
          ],
          "readable": false,
          "resolved_access": 1,
          "resolved_array_size": 3,
          "resolved_default": 3,
          "resolved_offset": 8,
          "resolved_read_permission": 0,
          "resolved_total_size": 3,
          "resolved_type": "uint8_t",
          "resolved_type_size": 1,
          "resolved_write_permission": 1,
          "type": "uint8_t",
          "use_bitfields": true,
          "use_defines": true,
          "use_enums": false,
          "writable": true,
          "write_permission": [
            "user"
          ]
        },
        {
          "array_size": "def_1",
          "default": "def_1",
          "map_offset": 10,
          "name": "record_3[2]",
          "read_permission": [
            0
          ],
          "readable": false,
          "resolved_access": 1,
          "resolved_array_size": 3,
          "resolved_default": 3,
          "resolved_offset": 8,
          "resolved_read_permission": 0,
          "resolved_total_size": 3,
          "resolved_type": "uint8_t",
          "resolved_type_size": 1,
          "resolved_write_permission": 1,
          "type": "uint8_t",
          "use_bitfields": true,
          "use_defines": true,
          "use_enums": false,
          "writable": true,
          "write_permission": [
            "user"
          ]
        },
        {
          "map_offset": 11,
          "name": "record_4.field_1",
          "read_permission": [
            0
          ],
          "readable": false,
          "resolved_access": 0,
          "resolved_bit_offset": 0,
          "resolved_bits": 1,
          "resolved_read_permission": 0,
          "resolved_type_size": 1,
          "resolved_write_permission": 0,
          "use_bitfields": true,
          "use_defines": true,
          "use_enums": false,
          "writable": false,
          "write_permission": [
            0
          ]
        },
        {
          "map_offset": 11,
          "name": "record_4.field_2",
          "read_permission": [
            0
          ],
          "readable": false,
          "resolved_access": 0,
          "resolved_bit_offset": 1,
          "resolved_bits": 1,
          "resolved_read_permission": 0,
          "resolved_type_size": 1,
          "resolved_write_permission": 0,
          "use_bitfields": true,
          "use_defines": true,
          "use_enums": false,
          "writable": false,
          "write_permission": [
            0
          ]
        },
        {
          "description": "padding bits",
          "map_offset": 11,
          "name": "record_4.padding",
          "read_permission": [
            0
          ],
          "readable": false,
          "reserved": true,
          "resolved_access": 0,
          "resolved_bit_offset": 2,
          "resolved_bits": 6,
          "resolved_read_permission": 0,
          "resolved_type_size": 1,
          "resolved_write_permission": 0,
          "use_bitfields": true,
          "use_defines": true,
          "use_enums": false,
          "writable": false,
          "write_permission": [
            0
          ]
        },
        {
          "map_offset": 12,
          "name": "record_5[0].field_1",
          "read_permission": [
            0
          ],
          "readable": false,
          "resolved_access": 0,
          "resolved_bit_offset": 0,
          "resolved_bits": 1,
          "resolved_read_permission": 0,
          "resolved_type_size": 1,
          "resolved_write_permission": 0,
          "use_bitfields": true,
          "use_defines": true,
          "use_enums": false,
          "writable": false,
          "write_permission": [
            0
          ]
        },
        {
          "map_offset": 12,
          "name": "record_5[0].field_2",
          "read_permission": [
            0
          ],
          "readable": false,
          "resolved_access": 0,
          "resolved_bit_offset": 1,
          "resolved_bits": 1,
          "resolved_read_permission": 0,
          "resolved_type_size": 1,
          "resolved_write_permission": 0,
          "use_bitfields": true,
          "use_defines": true,
          "use_enums": false,
          "writable": false,
          "write_permission": [
            0
          ]
        },
        {
          "description": "padding bits",
          "map_offset": 12,
          "name": "record_5[0].padding",
          "read_permission": [
            0
          ],
          "readable": false,
          "reserved": true,
          "resolved_access": 0,
          "resolved_bit_offset": 2,
          "resolved_bits": 6,
          "resolved_read_permission": 0,
          "resolved_type_size": 1,
          "resolved_write_permission": 0,
          "use_bitfields": true,
          "use_defines": true,
          "use_enums": false,
          "writable": false,
          "write_permission": [
            0
          ]
        },
        {
          "bits": 12,
          "map_offset": 13,
          "name": "record_6[0].field_1",
          "read_permission": [
            0
          ],
          "readable": false,
          "resolved_access": 0,
          "resolved_bit_offset": 0,
          "resolved_bits": 12,
          "resolved_read_permission": 0,
          "resolved_type_size": 2,
          "resolved_write_permission": 0,
          "use_bitfields": true,
          "use_defines": true,
          "use_enums": false,
          "writable": false,
          "write_permission": [
            0
          ]
        },
        {
          "description": "padding bits",
          "map_offset": 13,
          "name": "record_6[0].padding",
          "read_permission": [
            0
          ],
          "readable": false,
          "reserved": true,
          "resolved_access": 0,
          "resolved_bit_offset": 12,
          "resolved_bits": 4,
          "resolved_read_permission": 0,
          "resolved_type_size": 2,
          "resolved_write_permission": 0,
          "use_bitfields": true,
          "use_defines": true,
          "use_enums": false,
          "writable": false,
          "write_permission": [
            0
          ]
        },
        {
          "bits": 12,
          "map_offset": 15,
          "name": "record_6[1].field_1",
          "read_permission": [
            0
          ],
          "readable": false,
          "resolved_access": 0,
          "resolved_bit_offset": 0,
          "resolved_bits": 12,
          "resolved_read_permission": 0,
          "resolved_type_size": 2,
          "resolved_write_permission": 0,
          "use_bitfields": true,
          "use_defines": true,
          "use_enums": false,
          "writable": false,
          "write_permission": [
            0
          ]
        },
        {
          "description": "padding bits",
          "map_offset": 15,
          "name": "record_6[1].padding",
          "read_permission": [
            0
          ],
          "readable": false,
          "reserved": true,
          "resolved_access": 0,
          "resolved_bit_offset": 12,
          "resolved_bits": 4,
          "resolved_read_permission": 0,
          "resolved_type_size": 2,
          "resolved_write_permission": 0,
          "use_bitfields": true,
          "use_defines": true,
          "use_enums": false,
          "writable": false,
          "write_permission": [
            0
          ]
        },
        {
          "bits": 12,
          "map_offset": 17,
          "name": "record_6[2].field_1",
          "read_permission": [
            0
          ],
          "readable": false,
          "resolved_access": 0,
          "resolved_bit_offset": 0,
          "resolved_bits": 12,
          "resolved_read_permission": 0,
          "resolved_type_size": 2,
          "resolved_write_permission": 0,
          "use_bitfields": true,
          "use_defines": true,
          "use_enums": false,
          "writable": false,
          "write_permission": [
            0
          ]
        },
        {
          "description": "padding bits",
          "map_offset": 17,
          "name": "record_6[2].padding",
          "read_permission": [
            0
          ],
          "readable": false,
          "reserved": true,
          "resolved_access": 0,
          "resolved_bit_offset": 12,
          "resolved_bits": 4,
          "resolved_read_permission": 0,
          "resolved_type_size": 2,
          "resolved_write_permission": 0,
          "use_bitfields": true,
          "use_defines": true,
          "use_enums": false,
          "writable": false,
          "write_permission": [
            0
          ]
        },
        {
          "map_offset": 19,
          "name": "record_7.record_1",
          "read_permission": [
            0
          ],
          "readable": false,
          "resolved_access": 0,
          "resolved_offset": 0,
          "resolved_read_permission": 0,
          "resolved_total_size": 4,
          "resolved_type": "uint32_t",
          "resolved_type_size": 4,
          "resolved_write_permission": 0,
          "use_bitfields": false,
          "use_defines": false,
          "use_enums": false,
          "writable": false,
          "write_permission": [
            0
          ]
        },
        {
          "map_offset": 23,
          "name": "record_8[0].record_1",
          "read_permission": [
            0
          ],
          "readable": false,
          "resolved_access": 0,
          "resolved_offset": 0,
          "resolved_read_permission": 0,
          "resolved_total_size": 4,
          "resolved_type": "uint32_t",
          "resolved_type_size": 4,
          "resolved_write_permission": 0,
          "use_bitfields": false,
          "use_defines": false,
          "use_enums": false,
          "writable": false,
          "write_permission": [
            0
          ]
        },
        {
          "map_offset": 27,
          "name": "record_8[1].record_1",
          "read_permission": [
            0
          ],
          "readable": false,
          "resolved_access": 0,
          "resolved_offset": 0,
          "resolved_read_permission": 0,
          "resolved_total_size": 4,
          "resolved_type": "uint32_t",
          "resolved_type_size": 4,
          "resolved_write_permission": 0,
          "use_bitfields": false,
          "use_defines": false,
          "use_enums": false,
          "writable": false,
          "write_permission": [
            0
          ]
        },
        {
          "map_offset": 31,
          "name": "record_8[2].record_1",
          "read_permission": [
            0
          ],
          "readable": false,
          "resolved_access": 0,
          "resolved_offset": 0,
          "resolved_read_permission": 0,
          "resolved_total_size": 4,
          "resolved_type": "uint32_t",
          "resolved_type_size": 4,
          "resolved_write_permission": 0,
          "use_bitfields": false,
          "use_defines": false,
          "use_enums": false,
          "writable": false,
          "write_permission": [
            0
          ]
        },
        {
          "map_offset": 35,
          "name": "record_8[3].record_1",
          "read_permission": [
            0
          ],
          "readable": false,
          "resolved_access": 0,
          "resolved_offset": 0,
          "resolved_read_permission": 0,
          "resolved_total_size": 4,
          "resolved_type": "uint32_t",
          "resolved_type_size": 4,
          "resolved_write_permission": 0,
          "use_bitfields": false,
          "use_defines": false,
          "use_enums": false,
          "writable": false,
          "write_permission": [
            0
          ]
        },
        {
          "map_offset": 39,
          "name": "record_9[0].record_1",
          "read_permission": [
            0
          ],
          "readable": false,
          "resolved_access": 0,
          "resolved_offset": 0,
          "resolved_read_permission": 0,
          "resolved_total_size": 4,
          "resolved_type": "uint32_t",
          "resolved_type_size": 4,
          "resolved_write_permission": 0,
          "use_bitfields": false,
          "use_defines": false,
          "use_enums": false,
          "writable": false,
          "write_permission": [
            0
          ]
        },
        {
          "map_offset": 43,
          "name": "record_9[1].record_1",
          "read_permission": [
            0
          ],
          "readable": false,
          "resolved_access": 0,
          "resolved_offset": 0,
          "resolved_read_permission": 0,
          "resolved_total_size": 4,
          "resolved_type": "uint32_t",
          "resolved_type_size": 4,
          "resolved_write_permission": 0,
          "use_bitfields": false,
          "use_defines": false,
          "use_enums": false,
          "writable": false,
          "write_permission": [
            0
          ]
        },
        {
          "map_offset": 47,
          "name": "record_9[2].record_1",
          "read_permission": [
            0
          ],
          "readable": false,
          "resolved_access": 0,
          "resolved_offset": 0,
          "resolved_read_permission": 0,
          "resolved_total_size": 4,
          "resolved_type": "uint32_t",
          "resolved_type_size": 4,
          "resolved_write_permission": 0,
          "use_bitfields": false,
          "use_defines": false,
          "use_enums": false,
          "writable": false,
          "write_permission": [
            0
          ]
        }
      ],
      "type": "type_1"
    },
    "map_2": {
      "compressed_records": [
        {
          "compressed_info": [
            {
              "end": false,
              "idx_name": "n",
              "size": 2,
              "start": true,
              "uid": 7
            }
          ],
          "compressed_offset": "0+2*n",
          "default": 1,
          "map_offset": 0,
          "name": "record_1[n].record_1",
          "read_permission": [
            "user"
          ],
          "readable": true,
          "resolved_access": 17,
          "resolved_offset": 0,
          "resolved_read_permission": 1,
          "resolved_total_size": 4,
          "resolved_type": "uint32_t",
          "resolved_type_size": 4,
          "resolved_write_permission": 1,
          "type": "uint32_t",
          "use_bitfields": true,
          "use_defines": true,
          "use_enums": false,
          "writable": true,
          "write_permission": [
            "user"
          ]
        },
        {
          "array_size": 2,
          "compressed_info": [
            {
              "end": false,
              "idx_name": "n",
              "size": 2,
              "start": false,
              "uid": 7
            },
            {
              "end": true,
              "idx_name": "m",
              "size": 2,
              "start": true,
              "uid": 8
            }
          ],
          "compressed_offset": "4+2*n+2*m",
          "default": 2,
          "map_offset": 4,
          "name": "record_1[n].record_2[m]",
          "read_permission": [
            "user"
          ],
          "readable": true,
          "resolved_access": 16,
          "resolved_array_size": 2,
          "resolved_offset": 4,
          "resolved_read_permission": 1,
          "resolved_total_size": 4,
          "resolved_type": "uint16_t",
          "resolved_type_size": 2,
          "resolved_write_permission": 0,
          "type": "uint16_t",
          "use_bitfields": true,
          "use_defines": true,
          "use_enums": false,
          "writable": false,
          "write_permission": [
            0
          ]
        },
        {
          "array_size": "def_1",
          "compressed_info": [
            {
              "end": false,
              "idx_name": "n",
              "size": 2,
              "start": false,
              "uid": 7
            },
            {
              "end": true,
              "idx_name": "m",
              "size": 3,
              "start": true,
              "uid": 9
            }
          ],
          "compressed_offset": "8+2*n+3*m",
          "default": "def_1",
          "map_offset": 8,
          "name": "record_1[n].record_3[m]",
          "read_permission": [
            0
          ],
          "readable": false,
          "resolved_access": 1,
          "resolved_array_size": 3,
          "resolved_offset": 8,
          "resolved_read_permission": 0,
          "resolved_total_size": 3,
          "resolved_type": "uint8_t",
          "resolved_type_size": 1,
          "resolved_write_permission": 1,
          "type": "uint8_t",
          "use_bitfields": true,
          "use_defines": true,
          "use_enums": false,
          "writable": true,
          "write_permission": [
            "user"
          ]
        },
        {
          "compressed_info": [
            {
              "end": false,
              "idx_name": "n",
              "size": 2,
              "start": false,
              "uid": 7
            }
          ],
          "compressed_offset": "11+2*n",
          "map_offset": 11,
          "name": "record_1[n].record_4.field_1",
          "read_permission": [
            0
          ],
          "readable": false,
          "resolved_access": 0,
          "resolved_bit_offset": 0,
          "resolved_bits": 1,
          "resolved_read_permission": 0,
          "resolved_type_size": 1,
          "resolved_write_permission": 0,
          "use_bitfields": true,
          "use_defines": true,
          "use_enums": false,
          "writable": false,
          "write_permission": [
            0
          ]
        },
        {
          "compressed_info": [
            {
              "end": false,
              "idx_name": "n",
              "size": 2,
              "start": false,
              "uid": 7
            }
          ],
          "compressed_offset": "11+2*n",
          "map_offset": 11,
          "name": "record_1[n].record_4.field_2",
          "read_permission": [
            0
          ],
          "readable": false,
          "resolved_access": 0,
          "resolved_bit_offset": 1,
          "resolved_bits": 1,
          "resolved_read_permission": 0,
          "resolved_type_size": 1,
          "resolved_write_permission": 0,
          "use_bitfields": true,
          "use_defines": true,
          "use_enums": false,
          "writable": false,
          "write_permission": [
            0
          ]
        },
        {
          "compressed_info": [
            {
              "end": false,
              "idx_name": "n",
              "size": 2,
              "start": false,
              "uid": 7
            }
          ],
          "compressed_offset": "11+2*n",
          "description": "padding bits",
          "map_offset": 11,
          "name": "record_1[n].record_4.padding",
          "read_permission": [
            0
          ],
          "readable": false,
          "reserved": true,
          "resolved_access": 0,
          "resolved_bit_offset": 2,
          "resolved_bits": 6,
          "resolved_read_permission": 0,
          "resolved_type_size": 1,
          "resolved_write_permission": 0,
          "use_bitfields": true,
          "use_defines": true,
          "use_enums": false,
          "writable": false,
          "write_permission": [
            0
          ]
        },
        {
          "compressed_info": [
            {
              "end": false,
              "idx_name": "n",
              "size": 2,
              "start": false,
              "uid": 7
            },
            {
              "end": false,
              "idx_name": "m",
              "size": 1,
              "start": true,
              "uid": 10
            }
          ],
          "compressed_offset": "12+2*n+1*m",
          "map_offset": 12,
          "name": "record_1[n].record_5[m].field_1",
          "read_permission": [
            0
          ],
          "readable": false,
          "resolved_access": 0,
          "resolved_bit_offset": 0,
          "resolved_bits": 1,
          "resolved_read_permission": 0,
          "resolved_type_size": 1,
          "resolved_write_permission": 0,
          "use_bitfields": true,
          "use_defines": true,
          "use_enums": false,
          "writable": false,
          "write_permission": [
            0
          ]
        },
        {
          "compressed_info": [
            {
              "end": false,
              "idx_name": "n",
              "size": 2,
              "start": false,
              "uid": 7
            },
            {
              "end": false,
              "idx_name": "m",
              "size": 1,
              "start": false,
              "uid": 10
            }
          ],
          "compressed_offset": "12+2*n+1*m",
          "map_offset": 12,
          "name": "record_1[n].record_5[m].field_2",
          "read_permission": [
            0
          ],
          "readable": false,
          "resolved_access": 0,
          "resolved_bit_offset": 1,
          "resolved_bits": 1,
          "resolved_read_permission": 0,
          "resolved_type_size": 1,
          "resolved_write_permission": 0,
          "use_bitfields": true,
          "use_defines": true,
          "use_enums": false,
          "writable": false,
          "write_permission": [
            0
          ]
        },
        {
          "compressed_info": [
            {
              "end": false,
              "idx_name": "n",
              "size": 2,
              "start": false,
              "uid": 7
            },
            {
              "end": true,
              "idx_name": "m",
              "size": 1,
              "start": false,
              "uid": 10
            }
          ],
          "compressed_offset": "12+2*n+1*m",
          "description": "padding bits",
          "map_offset": 12,
          "name": "record_1[n].record_5[m].padding",
          "read_permission": [
            0
          ],
          "readable": false,
          "reserved": true,
          "resolved_access": 0,
          "resolved_bit_offset": 2,
          "resolved_bits": 6,
          "resolved_read_permission": 0,
          "resolved_type_size": 1,
          "resolved_write_permission": 0,
          "use_bitfields": true,
          "use_defines": true,
          "use_enums": false,
          "writable": false,
          "write_permission": [
            0
          ]
        },
        {
          "bits": 12,
          "compressed_info": [
            {
              "end": false,
              "idx_name": "n",
              "size": 2,
              "start": false,
              "uid": 7
            },
            {
              "end": false,
              "idx_name": "m",
              "size": 3,
              "start": true,
              "uid": 11
            }
          ],
          "compressed_offset": "13+2*n+3*m",
          "map_offset": 13,
          "name": "record_1[n].record_6[m].field_1",
          "read_permission": [
            0
          ],
          "readable": false,
          "resolved_access": 0,
          "resolved_bit_offset": 0,
          "resolved_bits": 12,
          "resolved_read_permission": 0,
          "resolved_type_size": 2,
          "resolved_write_permission": 0,
          "use_bitfields": true,
          "use_defines": true,
          "use_enums": false,
          "writable": false,
          "write_permission": [
            0
          ]
        },
        {
          "compressed_info": [
            {
              "end": false,
              "idx_name": "n",
              "size": 2,
              "start": false,
              "uid": 7
            },
            {
              "end": true,
              "idx_name": "m",
              "size": 3,
              "start": false,
              "uid": 11
            }
          ],
          "compressed_offset": "13+2*n+3*m",
          "description": "padding bits",
          "map_offset": 13,
          "name": "record_1[n].record_6[m].padding",
          "read_permission": [
            0
          ],
          "readable": false,
          "reserved": true,
          "resolved_access": 0,
          "resolved_bit_offset": 12,
          "resolved_bits": 4,
          "resolved_read_permission": 0,
          "resolved_type_size": 2,
          "resolved_write_permission": 0,
          "use_bitfields": true,
          "use_defines": true,
          "use_enums": false,
          "writable": false,
          "write_permission": [
            0
          ]
        },
        {
          "compressed_info": [
            {
              "end": false,
              "idx_name": "n",
              "size": 2,
              "start": false,
              "uid": 7
            }
          ],
          "compressed_offset": "19+2*n",
          "map_offset": 19,
          "name": "record_1[n].record_7.record_1",
          "read_permission": [
            0
          ],
          "readable": false,
          "resolved_access": 0,
          "resolved_offset": 0,
          "resolved_read_permission": 0,
          "resolved_total_size": 4,
          "resolved_type": "uint32_t",
          "resolved_type_size": 4,
          "resolved_write_permission": 0,
          "use_bitfields": false,
          "use_defines": false,
          "use_enums": false,
          "writable": false,
          "write_permission": [
            0
          ]
        },
        {
          "compressed_info": [
            {
              "end": false,
              "idx_name": "n",
              "size": 2,
              "start": false,
              "uid": 7
            },
            {
              "end": true,
              "idx_name": "m",
              "size": 4,
              "start": true,
              "uid": 12
            }
          ],
          "compressed_offset": "23+2*n+4*m",
          "map_offset": 23,
          "name": "record_1[n].record_8[m].record_1",
          "read_permission": [
            0
          ],
          "readable": false,
          "resolved_access": 0,
          "resolved_offset": 0,
          "resolved_read_permission": 0,
          "resolved_total_size": 4,
          "resolved_type": "uint32_t",
          "resolved_type_size": 4,
          "resolved_write_permission": 0,
          "use_bitfields": false,
          "use_defines": false,
          "use_enums": false,
          "writable": false,
          "write_permission": [
            0
          ]
        },
        {
          "compressed_info": [
            {
              "end": true,
              "idx_name": "n",
              "size": 2,
              "start": false,
              "uid": 7
            },
            {
              "end": true,
              "idx_name": "m",
              "size": 3,
              "start": true,
              "uid": 13
            }
          ],
          "compressed_offset": "39+2*n+3*m",
          "map_offset": 39,
          "name": "record_1[n].record_9[m].record_1",
          "read_permission": [
            0
          ],
          "readable": false,
          "resolved_access": 0,
          "resolved_offset": 0,
          "resolved_read_permission": 0,
          "resolved_total_size": 4,
          "resolved_type": "uint32_t",
          "resolved_type_size": 4,
          "resolved_write_permission": 0,
          "use_bitfields": false,
          "use_defines": false,
          "use_enums": false,
          "writable": false,
          "write_permission": [
            0
          ]
        }
      ],
      "records": [
        {
          "default": 1,
          "map_offset": 0,
          "name": "record_1[0].record_1",
          "read_permission": [
            "user"
          ],
          "readable": true,
          "resolved_access": 17,
          "resolved_default": 1,
          "resolved_offset": 0,
          "resolved_read_permission": 1,
          "resolved_total_size": 4,
          "resolved_type": "uint32_t",
          "resolved_type_size": 4,
          "resolved_write_permission": 1,
          "type": "uint32_t",
          "use_bitfields": true,
          "use_defines": true,
          "use_enums": false,
          "writable": true,
          "write_permission": [
            "user"
          ]
        },
        {
          "array_size": 2,
          "default": 2,
          "map_offset": 4,
          "name": "record_1[0].record_2[0]",
          "read_permission": [
            "user"
          ],
          "readable": true,
          "resolved_access": 16,
          "resolved_array_size": 2,
          "resolved_default": 2,
          "resolved_offset": 4,
          "resolved_read_permission": 1,
          "resolved_total_size": 4,
          "resolved_type": "uint16_t",
          "resolved_type_size": 2,
          "resolved_write_permission": 0,
          "type": "uint16_t",
          "use_bitfields": true,
          "use_defines": true,
          "use_enums": false,
          "writable": false,
          "write_permission": [
            0
          ]
        },
        {
          "array_size": 2,
          "default": 2,
          "map_offset": 6,
          "name": "record_1[0].record_2[1]",
          "read_permission": [
            "user"
          ],
          "readable": true,
          "resolved_access": 16,
          "resolved_array_size": 2,
          "resolved_default": 2,
          "resolved_offset": 4,
          "resolved_read_permission": 1,
          "resolved_total_size": 4,
          "resolved_type": "uint16_t",
          "resolved_type_size": 2,
          "resolved_write_permission": 0,
          "type": "uint16_t",
          "use_bitfields": true,
          "use_defines": true,
          "use_enums": false,
          "writable": false,
          "write_permission": [
            0
          ]
        },
        {
          "array_size": "def_1",
          "default": "def_1",
          "map_offset": 8,
          "name": "record_1[0].record_3[0]",
          "read_permission": [
            0
          ],
          "readable": false,
          "resolved_access": 1,
          "resolved_array_size": 3,
          "resolved_default": 3,
          "resolved_offset": 8,
          "resolved_read_permission": 0,
          "resolved_total_size": 3,
          "resolved_type": "uint8_t",
          "resolved_type_size": 1,
          "resolved_write_permission": 1,
          "type": "uint8_t",
          "use_bitfields": true,
          "use_defines": true,
          "use_enums": false,
          "writable": true,
          "write_permission": [
            "user"
          ]
        },
        {
          "array_size": "def_1",
          "default": "def_1",
          "map_offset": 9,
          "name": "record_1[0].record_3[1]",
          "read_permission": [
            0
          ],
          "readable": false,
          "resolved_access": 1,
          "resolved_array_size": 3,
          "resolved_default": 3,
          "resolved_offset": 8,
          "resolved_read_permission": 0,
          "resolved_total_size": 3,
          "resolved_type": "uint8_t",
          "resolved_type_size": 1,
          "resolved_write_permission": 1,
          "type": "uint8_t",
          "use_bitfields": true,
          "use_defines": true,
          "use_enums": false,
          "writable": true,
          "write_permission": [
            "user"
          ]
        },
        {
          "array_size": "def_1",
          "default": "def_1",
          "map_offset": 10,
          "name": "record_1[0].record_3[2]",
          "read_permission": [
            0
          ],
          "readable": false,
          "resolved_access": 1,
          "resolved_array_size": 3,
          "resolved_default": 3,
          "resolved_offset": 8,
          "resolved_read_permission": 0,
          "resolved_total_size": 3,
          "resolved_type": "uint8_t",
          "resolved_type_size": 1,
          "resolved_write_permission": 1,
          "type": "uint8_t",
          "use_bitfields": true,
          "use_defines": true,
          "use_enums": false,
          "writable": true,
          "write_permission": [
            "user"
          ]
        },
        {
          "map_offset": 11,
          "name": "record_1[0].record_4.field_1",
          "read_permission": [
            0
          ],
          "readable": false,
          "resolved_access": 0,
          "resolved_bit_offset": 0,
          "resolved_bits": 1,
          "resolved_read_permission": 0,
          "resolved_type_size": 1,
          "resolved_write_permission": 0,
          "use_bitfields": true,
          "use_defines": true,
          "use_enums": false,
          "writable": false,
          "write_permission": [
            0
          ]
        },
        {
          "map_offset": 11,
          "name": "record_1[0].record_4.field_2",
          "read_permission": [
            0
          ],
          "readable": false,
          "resolved_access": 0,
          "resolved_bit_offset": 1,
          "resolved_bits": 1,
          "resolved_read_permission": 0,
          "resolved_type_size": 1,
          "resolved_write_permission": 0,
          "use_bitfields": true,
          "use_defines": true,
          "use_enums": false,
          "writable": false,
          "write_permission": [
            0
          ]
        },
        {
          "description": "padding bits",
          "map_offset": 11,
          "name": "record_1[0].record_4.padding",
          "read_permission": [
            0
          ],
          "readable": false,
          "reserved": true,
          "resolved_access": 0,
          "resolved_bit_offset": 2,
          "resolved_bits": 6,
          "resolved_read_permission": 0,
          "resolved_type_size": 1,
          "resolved_write_permission": 0,
          "use_bitfields": true,
          "use_defines": true,
          "use_enums": false,
          "writable": false,
          "write_permission": [
            0
          ]
        },
        {
          "map_offset": 12,
          "name": "record_1[0].record_5[0].field_1",
          "read_permission": [
            0
          ],
          "readable": false,
          "resolved_access": 0,
          "resolved_bit_offset": 0,
          "resolved_bits": 1,
          "resolved_read_permission": 0,
          "resolved_type_size": 1,
          "resolved_write_permission": 0,
          "use_bitfields": true,
          "use_defines": true,
          "use_enums": false,
          "writable": false,
          "write_permission": [
            0
          ]
        },
        {
          "map_offset": 12,
          "name": "record_1[0].record_5[0].field_2",
          "read_permission": [
            0
          ],
          "readable": false,
          "resolved_access": 0,
          "resolved_bit_offset": 1,
          "resolved_bits": 1,
          "resolved_read_permission": 0,
          "resolved_type_size": 1,
          "resolved_write_permission": 0,
          "use_bitfields": true,
          "use_defines": true,
          "use_enums": false,
          "writable": false,
          "write_permission": [
            0
          ]
        },
        {
          "description": "padding bits",
          "map_offset": 12,
          "name": "record_1[0].record_5[0].padding",
          "read_permission": [
            0
          ],
          "readable": false,
          "reserved": true,
          "resolved_access": 0,
          "resolved_bit_offset": 2,
          "resolved_bits": 6,
          "resolved_read_permission": 0,
          "resolved_type_size": 1,
          "resolved_write_permission": 0,
          "use_bitfields": true,
          "use_defines": true,
          "use_enums": false,
          "writable": false,
          "write_permission": [
            0
          ]
        },
        {
          "bits": 12,
          "map_offset": 13,
          "name": "record_1[0].record_6[0].field_1",
          "read_permission": [
            0
          ],
          "readable": false,
          "resolved_access": 0,
          "resolved_bit_offset": 0,
          "resolved_bits": 12,
          "resolved_read_permission": 0,
          "resolved_type_size": 2,
          "resolved_write_permission": 0,
          "use_bitfields": true,
          "use_defines": true,
          "use_enums": false,
          "writable": false,
          "write_permission": [
            0
          ]
        },
        {
          "description": "padding bits",
          "map_offset": 13,
          "name": "record_1[0].record_6[0].padding",
          "read_permission": [
            0
          ],
          "readable": false,
          "reserved": true,
          "resolved_access": 0,
          "resolved_bit_offset": 12,
          "resolved_bits": 4,
          "resolved_read_permission": 0,
          "resolved_type_size": 2,
          "resolved_write_permission": 0,
          "use_bitfields": true,
          "use_defines": true,
          "use_enums": false,
          "writable": false,
          "write_permission": [
            0
          ]
        },
        {
          "bits": 12,
          "map_offset": 15,
          "name": "record_1[0].record_6[1].field_1",
          "read_permission": [
            0
          ],
          "readable": false,
          "resolved_access": 0,
          "resolved_bit_offset": 0,
          "resolved_bits": 12,
          "resolved_read_permission": 0,
          "resolved_type_size": 2,
          "resolved_write_permission": 0,
          "use_bitfields": true,
          "use_defines": true,
          "use_enums": false,
          "writable": false,
          "write_permission": [
            0
          ]
        },
        {
          "description": "padding bits",
          "map_offset": 15,
          "name": "record_1[0].record_6[1].padding",
          "read_permission": [
            0
          ],
          "readable": false,
          "reserved": true,
          "resolved_access": 0,
          "resolved_bit_offset": 12,
          "resolved_bits": 4,
          "resolved_read_permission": 0,
          "resolved_type_size": 2,
          "resolved_write_permission": 0,
          "use_bitfields": true,
          "use_defines": true,
          "use_enums": false,
          "writable": false,
          "write_permission": [
            0
          ]
        },
        {
          "bits": 12,
          "map_offset": 17,
          "name": "record_1[0].record_6[2].field_1",
          "read_permission": [
            0
          ],
          "readable": false,
          "resolved_access": 0,
          "resolved_bit_offset": 0,
          "resolved_bits": 12,
          "resolved_read_permission": 0,
          "resolved_type_size": 2,
          "resolved_write_permission": 0,
          "use_bitfields": true,
          "use_defines": true,
          "use_enums": false,
          "writable": false,
          "write_permission": [
            0
          ]
        },
        {
          "description": "padding bits",
          "map_offset": 17,
          "name": "record_1[0].record_6[2].padding",
          "read_permission": [
            0
          ],
          "readable": false,
          "reserved": true,
          "resolved_access": 0,
          "resolved_bit_offset": 12,
          "resolved_bits": 4,
          "resolved_read_permission": 0,
          "resolved_type_size": 2,
          "resolved_write_permission": 0,
          "use_bitfields": true,
          "use_defines": true,
          "use_enums": false,
          "writable": false,
          "write_permission": [
            0
          ]
        },
        {
          "map_offset": 19,
          "name": "record_1[0].record_7.record_1",
          "read_permission": [
            0
          ],
          "readable": false,
          "resolved_access": 0,
          "resolved_offset": 0,
          "resolved_read_permission": 0,
          "resolved_total_size": 4,
          "resolved_type": "uint32_t",
          "resolved_type_size": 4,
          "resolved_write_permission": 0,
          "use_bitfields": false,
          "use_defines": false,
          "use_enums": false,
          "writable": false,
          "write_permission": [
            0
          ]
        },
        {
          "map_offset": 23,
          "name": "record_1[0].record_8[0].record_1",
          "read_permission": [
            0
          ],
          "readable": false,
          "resolved_access": 0,
          "resolved_offset": 0,
          "resolved_read_permission": 0,
          "resolved_total_size": 4,
          "resolved_type": "uint32_t",
          "resolved_type_size": 4,
          "resolved_write_permission": 0,
          "use_bitfields": false,
          "use_defines": false,
          "use_enums": false,
          "writable": false,
          "write_permission": [
            0
          ]
        },
        {
          "map_offset": 27,
          "name": "record_1[0].record_8[1].record_1",
          "read_permission": [
            0
          ],
          "readable": false,
          "resolved_access": 0,
          "resolved_offset": 0,
          "resolved_read_permission": 0,
          "resolved_total_size": 4,
          "resolved_type": "uint32_t",
          "resolved_type_size": 4,
          "resolved_write_permission": 0,
          "use_bitfields": false,
          "use_defines": false,
          "use_enums": false,
          "writable": false,
          "write_permission": [
            0
          ]
        },
        {
          "map_offset": 31,
          "name": "record_1[0].record_8[2].record_1",
          "read_permission": [
            0
          ],
          "readable": false,
          "resolved_access": 0,
          "resolved_offset": 0,
          "resolved_read_permission": 0,
          "resolved_total_size": 4,
          "resolved_type": "uint32_t",
          "resolved_type_size": 4,
          "resolved_write_permission": 0,
          "use_bitfields": false,
          "use_defines": false,
          "use_enums": false,
          "writable": false,
          "write_permission": [
            0
          ]
        },
        {
          "map_offset": 35,
          "name": "record_1[0].record_8[3].record_1",
          "read_permission": [
            0
          ],
          "readable": false,
          "resolved_access": 0,
          "resolved_offset": 0,
          "resolved_read_permission": 0,
          "resolved_total_size": 4,
          "resolved_type": "uint32_t",
          "resolved_type_size": 4,
          "resolved_write_permission": 0,
          "use_bitfields": false,
          "use_defines": false,
          "use_enums": false,
          "writable": false,
          "write_permission": [
            0
          ]
        },
        {
          "map_offset": 39,
          "name": "record_1[0].record_9[0].record_1",
          "read_permission": [
            0
          ],
          "readable": false,
          "resolved_access": 0,
          "resolved_offset": 0,
          "resolved_read_permission": 0,
          "resolved_total_size": 4,
          "resolved_type": "uint32_t",
          "resolved_type_size": 4,
          "resolved_write_permission": 0,
          "use_bitfields": false,
          "use_defines": false,
          "use_enums": false,
          "writable": false,
          "write_permission": [
            0
          ]
        },
        {
          "map_offset": 43,
          "name": "record_1[0].record_9[1].record_1",
          "read_permission": [
            0
          ],
          "readable": false,
          "resolved_access": 0,
          "resolved_offset": 0,
          "resolved_read_permission": 0,
          "resolved_total_size": 4,
          "resolved_type": "uint32_t",
          "resolved_type_size": 4,
          "resolved_write_permission": 0,
          "use_bitfields": false,
          "use_defines": false,
          "use_enums": false,
          "writable": false,
          "write_permission": [
            0
          ]
        },
        {
          "map_offset": 47,
          "name": "record_1[0].record_9[2].record_1",
          "read_permission": [
            0
          ],
          "readable": false,
          "resolved_access": 0,
          "resolved_offset": 0,
          "resolved_read_permission": 0,
          "resolved_total_size": 4,
          "resolved_type": "uint32_t",
          "resolved_type_size": 4,
          "resolved_write_permission": 0,
          "use_bitfields": false,
          "use_defines": false,
          "use_enums": false,
          "writable": false,
          "write_permission": [
            0
          ]
        },
        {
          "default": 1,
          "map_offset": 51,
          "name": "record_1[1].record_1",
          "read_permission": [
            "user"
          ],
          "readable": true,
          "resolved_access": 17,
          "resolved_default": 1,
          "resolved_offset": 0,
          "resolved_read_permission": 1,
          "resolved_total_size": 4,
          "resolved_type": "uint32_t",
          "resolved_type_size": 4,
          "resolved_write_permission": 1,
          "type": "uint32_t",
          "use_bitfields": true,
          "use_defines": true,
          "use_enums": false,
          "writable": true,
          "write_permission": [
            "user"
          ]
        },
        {
          "array_size": 2,
          "default": 2,
          "map_offset": 55,
          "name": "record_1[1].record_2[0]",
          "read_permission": [
            "user"
          ],
          "readable": true,
          "resolved_access": 16,
          "resolved_array_size": 2,
          "resolved_default": 2,
          "resolved_offset": 4,
          "resolved_read_permission": 1,
          "resolved_total_size": 4,
          "resolved_type": "uint16_t",
          "resolved_type_size": 2,
          "resolved_write_permission": 0,
          "type": "uint16_t",
          "use_bitfields": true,
          "use_defines": true,
          "use_enums": false,
          "writable": false,
          "write_permission": [
            0
          ]
        },
        {
          "array_size": 2,
          "default": 2,
          "map_offset": 57,
          "name": "record_1[1].record_2[1]",
          "read_permission": [
            "user"
          ],
          "readable": true,
          "resolved_access": 16,
          "resolved_array_size": 2,
          "resolved_default": 2,
          "resolved_offset": 4,
          "resolved_read_permission": 1,
          "resolved_total_size": 4,
          "resolved_type": "uint16_t",
          "resolved_type_size": 2,
          "resolved_write_permission": 0,
          "type": "uint16_t",
          "use_bitfields": true,
          "use_defines": true,
          "use_enums": false,
          "writable": false,
          "write_permission": [
            0
          ]
        },
        {
          "array_size": "def_1",
          "default": "def_1",
          "map_offset": 59,
          "name": "record_1[1].record_3[0]",
          "read_permission": [
            0
          ],
          "readable": false,
          "resolved_access": 1,
          "resolved_array_size": 3,
          "resolved_default": 3,
          "resolved_offset": 8,
          "resolved_read_permission": 0,
          "resolved_total_size": 3,
          "resolved_type": "uint8_t",
          "resolved_type_size": 1,
          "resolved_write_permission": 1,
          "type": "uint8_t",
          "use_bitfields": true,
          "use_defines": true,
          "use_enums": false,
          "writable": true,
          "write_permission": [
            "user"
          ]
        },
        {
          "array_size": "def_1",
          "default": "def_1",
          "map_offset": 60,
          "name": "record_1[1].record_3[1]",
          "read_permission": [
            0
          ],
          "readable": false,
          "resolved_access": 1,
          "resolved_array_size": 3,
          "resolved_default": 3,
          "resolved_offset": 8,
          "resolved_read_permission": 0,
          "resolved_total_size": 3,
          "resolved_type": "uint8_t",
          "resolved_type_size": 1,
          "resolved_write_permission": 1,
          "type": "uint8_t",
          "use_bitfields": true,
          "use_defines": true,
          "use_enums": false,
          "writable": true,
          "write_permission": [
            "user"
          ]
        },
        {
          "array_size": "def_1",
          "default": "def_1",
          "map_offset": 61,
          "name": "record_1[1].record_3[2]",
          "read_permission": [
            0
          ],
          "readable": false,
          "resolved_access": 1,
          "resolved_array_size": 3,
          "resolved_default": 3,
          "resolved_offset": 8,
          "resolved_read_permission": 0,
          "resolved_total_size": 3,
          "resolved_type": "uint8_t",
          "resolved_type_size": 1,
          "resolved_write_permission": 1,
          "type": "uint8_t",
          "use_bitfields": true,
          "use_defines": true,
          "use_enums": false,
          "writable": true,
          "write_permission": [
            "user"
          ]
        },
        {
          "map_offset": 62,
          "name": "record_1[1].record_4.field_1",
          "read_permission": [
            0
          ],
          "readable": false,
          "resolved_access": 0,
          "resolved_bit_offset": 0,
          "resolved_bits": 1,
          "resolved_read_permission": 0,
          "resolved_type_size": 1,
          "resolved_write_permission": 0,
          "use_bitfields": true,
          "use_defines": true,
          "use_enums": false,
          "writable": false,
          "write_permission": [
            0
          ]
        },
        {
          "map_offset": 62,
          "name": "record_1[1].record_4.field_2",
          "read_permission": [
            0
          ],
          "readable": false,
          "resolved_access": 0,
          "resolved_bit_offset": 1,
          "resolved_bits": 1,
          "resolved_read_permission": 0,
          "resolved_type_size": 1,
          "resolved_write_permission": 0,
          "use_bitfields": true,
          "use_defines": true,
          "use_enums": false,
          "writable": false,
          "write_permission": [
            0
          ]
        },
        {
          "description": "padding bits",
          "map_offset": 62,
          "name": "record_1[1].record_4.padding",
          "read_permission": [
            0
          ],
          "readable": false,
          "reserved": true,
          "resolved_access": 0,
          "resolved_bit_offset": 2,
          "resolved_bits": 6,
          "resolved_read_permission": 0,
          "resolved_type_size": 1,
          "resolved_write_permission": 0,
          "use_bitfields": true,
          "use_defines": true,
          "use_enums": false,
          "writable": false,
          "write_permission": [
            0
          ]
        },
        {
          "map_offset": 63,
          "name": "record_1[1].record_5[0].field_1",
          "read_permission": [
            0
          ],
          "readable": false,
          "resolved_access": 0,
          "resolved_bit_offset": 0,
          "resolved_bits": 1,
          "resolved_read_permission": 0,
          "resolved_type_size": 1,
          "resolved_write_permission": 0,
          "use_bitfields": true,
          "use_defines": true,
          "use_enums": false,
          "writable": false,
          "write_permission": [
            0
          ]
        },
        {
          "map_offset": 63,
          "name": "record_1[1].record_5[0].field_2",
          "read_permission": [
            0
          ],
          "readable": false,
          "resolved_access": 0,
          "resolved_bit_offset": 1,
          "resolved_bits": 1,
          "resolved_read_permission": 0,
          "resolved_type_size": 1,
          "resolved_write_permission": 0,
          "use_bitfields": true,
          "use_defines": true,
          "use_enums": false,
          "writable": false,
          "write_permission": [
            0
          ]
        },
        {
          "description": "padding bits",
          "map_offset": 63,
          "name": "record_1[1].record_5[0].padding",
          "read_permission": [
            0
          ],
          "readable": false,
          "reserved": true,
          "resolved_access": 0,
          "resolved_bit_offset": 2,
          "resolved_bits": 6,
          "resolved_read_permission": 0,
          "resolved_type_size": 1,
          "resolved_write_permission": 0,
          "use_bitfields": true,
          "use_defines": true,
          "use_enums": false,
          "writable": false,
          "write_permission": [
            0
          ]
        },
        {
          "bits": 12,
          "map_offset": 64,
          "name": "record_1[1].record_6[0].field_1",
          "read_permission": [
            0
          ],
          "readable": false,
          "resolved_access": 0,
          "resolved_bit_offset": 0,
          "resolved_bits": 12,
          "resolved_read_permission": 0,
          "resolved_type_size": 2,
          "resolved_write_permission": 0,
          "use_bitfields": true,
          "use_defines": true,
          "use_enums": false,
          "writable": false,
          "write_permission": [
            0
          ]
        },
        {
          "description": "padding bits",
          "map_offset": 64,
          "name": "record_1[1].record_6[0].padding",
          "read_permission": [
            0
          ],
          "readable": false,
          "reserved": true,
          "resolved_access": 0,
          "resolved_bit_offset": 12,
          "resolved_bits": 4,
          "resolved_read_permission": 0,
          "resolved_type_size": 2,
          "resolved_write_permission": 0,
          "use_bitfields": true,
          "use_defines": true,
          "use_enums": false,
          "writable": false,
          "write_permission": [
            0
          ]
        },
        {
          "bits": 12,
          "map_offset": 66,
          "name": "record_1[1].record_6[1].field_1",
          "read_permission": [
            0
          ],
          "readable": false,
          "resolved_access": 0,
          "resolved_bit_offset": 0,
          "resolved_bits": 12,
          "resolved_read_permission": 0,
          "resolved_type_size": 2,
          "resolved_write_permission": 0,
          "use_bitfields": true,
          "use_defines": true,
          "use_enums": false,
          "writable": false,
          "write_permission": [
            0
          ]
        },
        {
          "description": "padding bits",
          "map_offset": 66,
          "name": "record_1[1].record_6[1].padding",
          "read_permission": [
            0
          ],
          "readable": false,
          "reserved": true,
          "resolved_access": 0,
          "resolved_bit_offset": 12,
          "resolved_bits": 4,
          "resolved_read_permission": 0,
          "resolved_type_size": 2,
          "resolved_write_permission": 0,
          "use_bitfields": true,
          "use_defines": true,
          "use_enums": false,
          "writable": false,
          "write_permission": [
            0
          ]
        },
        {
          "bits": 12,
          "map_offset": 68,
          "name": "record_1[1].record_6[2].field_1",
          "read_permission": [
            0
          ],
          "readable": false,
          "resolved_access": 0,
          "resolved_bit_offset": 0,
          "resolved_bits": 12,
          "resolved_read_permission": 0,
          "resolved_type_size": 2,
          "resolved_write_permission": 0,
          "use_bitfields": true,
          "use_defines": true,
          "use_enums": false,
          "writable": false,
          "write_permission": [
            0
          ]
        },
        {
          "description": "padding bits",
          "map_offset": 68,
          "name": "record_1[1].record_6[2].padding",
          "read_permission": [
            0
          ],
          "readable": false,
          "reserved": true,
          "resolved_access": 0,
          "resolved_bit_offset": 12,
          "resolved_bits": 4,
          "resolved_read_permission": 0,
          "resolved_type_size": 2,
          "resolved_write_permission": 0,
          "use_bitfields": true,
          "use_defines": true,
          "use_enums": false,
          "writable": false,
          "write_permission": [
            0
          ]
        },
        {
          "map_offset": 70,
          "name": "record_1[1].record_7.record_1",
          "read_permission": [
            0
          ],
          "readable": false,
          "resolved_access": 0,
          "resolved_offset": 0,
          "resolved_read_permission": 0,
          "resolved_total_size": 4,
          "resolved_type": "uint32_t",
          "resolved_type_size": 4,
          "resolved_write_permission": 0,
          "use_bitfields": false,
          "use_defines": false,
          "use_enums": false,
          "writable": false,
          "write_permission": [
            0
          ]
        },
        {
          "map_offset": 74,
          "name": "record_1[1].record_8[0].record_1",
          "read_permission": [
            0
          ],
          "readable": false,
          "resolved_access": 0,
          "resolved_offset": 0,
          "resolved_read_permission": 0,
          "resolved_total_size": 4,
          "resolved_type": "uint32_t",
          "resolved_type_size": 4,
          "resolved_write_permission": 0,
          "use_bitfields": false,
          "use_defines": false,
          "use_enums": false,
          "writable": false,
          "write_permission": [
            0
          ]
        },
        {
          "map_offset": 78,
          "name": "record_1[1].record_8[1].record_1",
          "read_permission": [
            0
          ],
          "readable": false,
          "resolved_access": 0,
          "resolved_offset": 0,
          "resolved_read_permission": 0,
          "resolved_total_size": 4,
          "resolved_type": "uint32_t",
          "resolved_type_size": 4,
          "resolved_write_permission": 0,
          "use_bitfields": false,
          "use_defines": false,
          "use_enums": false,
          "writable": false,
          "write_permission": [
            0
          ]
        },
        {
          "map_offset": 82,
          "name": "record_1[1].record_8[2].record_1",
          "read_permission": [
            0
          ],
          "readable": false,
          "resolved_access": 0,
          "resolved_offset": 0,
          "resolved_read_permission": 0,
          "resolved_total_size": 4,
          "resolved_type": "uint32_t",
          "resolved_type_size": 4,
          "resolved_write_permission": 0,
          "use_bitfields": false,
          "use_defines": false,
          "use_enums": false,
          "writable": false,
          "write_permission": [
            0
          ]
        },
        {
          "map_offset": 86,
          "name": "record_1[1].record_8[3].record_1",
          "read_permission": [
            0
          ],
          "readable": false,
          "resolved_access": 0,
          "resolved_offset": 0,
          "resolved_read_permission": 0,
          "resolved_total_size": 4,
          "resolved_type": "uint32_t",
          "resolved_type_size": 4,
          "resolved_write_permission": 0,
          "use_bitfields": false,
          "use_defines": false,
          "use_enums": false,
          "writable": false,
          "write_permission": [
            0
          ]
        },
        {
          "map_offset": 90,
          "name": "record_1[1].record_9[0].record_1",
          "read_permission": [
            0
          ],
          "readable": false,
          "resolved_access": 0,
          "resolved_offset": 0,
          "resolved_read_permission": 0,
          "resolved_total_size": 4,
          "resolved_type": "uint32_t",
          "resolved_type_size": 4,
          "resolved_write_permission": 0,
          "use_bitfields": false,
          "use_defines": false,
          "use_enums": false,
          "writable": false,
          "write_permission": [
            0
          ]
        },
        {
          "map_offset": 94,
          "name": "record_1[1].record_9[1].record_1",
          "read_permission": [
            0
          ],
          "readable": false,
          "resolved_access": 0,
          "resolved_offset": 0,
          "resolved_read_permission": 0,
          "resolved_total_size": 4,
          "resolved_type": "uint32_t",
          "resolved_type_size": 4,
          "resolved_write_permission": 0,
          "use_bitfields": false,
          "use_defines": false,
          "use_enums": false,
          "writable": false,
          "write_permission": [
            0
          ]
        },
        {
          "map_offset": 98,
          "name": "record_1[1].record_9[2].record_1",
          "read_permission": [
            0
          ],
          "readable": false,
          "resolved_access": 0,
          "resolved_offset": 0,
          "resolved_read_permission": 0,
          "resolved_total_size": 4,
          "resolved_type": "uint32_t",
          "resolved_type_size": 4,
          "resolved_write_permission": 0,
          "use_bitfields": false,
          "use_defines": false,
          "use_enums": false,
          "writable": false,
          "write_permission": [
            0
          ]
        }
      ],
      "type": "type_3"
    },
    "map_3": {
      "compressed_records": [
        {
          "array_size": 2,
          "compressed_info": [
            {
              "end": true,
              "idx_name": "n",
              "size": 3,
              "start": true,
              "uid": 20
            },
            {
              "end": true,
              "idx_name": "m",
              "size": 2,
              "start": true,
              "uid": 21
            }
          ],
          "compressed_offset": "0+3*n+2*m",
          "map_offset": 0,
          "name": "record_1[n].record_1[m]",
          "read_permission": [
            0
          ],
          "readable": false,
          "resolved_access": 0,
          "resolved_array_size": 2,
          "resolved_offset": 0,
          "resolved_read_permission": 0,
          "resolved_total_size": 4,
          "resolved_type": "uint16_t",
          "resolved_type_size": 2,
          "resolved_write_permission": 0,
          "type": "uint16_t",
          "use_bitfields": false,
          "use_defines": false,
          "use_enums": false,
          "writable": false,
          "write_permission": [
            0
          ]
        }
      ],
      "records": [
        {
          "array_size": 2,
          "map_offset": 0,
          "name": "record_1[0].record_1[0]",
          "read_permission": [
            0
          ],
          "readable": false,
          "resolved_access": 0,
          "resolved_array_size": 2,
          "resolved_offset": 0,
          "resolved_read_permission": 0,
          "resolved_total_size": 4,
          "resolved_type": "uint16_t",
          "resolved_type_size": 2,
          "resolved_write_permission": 0,
          "type": "uint16_t",
          "use_bitfields": false,
          "use_defines": false,
          "use_enums": false,
          "writable": false,
          "write_permission": [
            0
          ]
        },
        {
          "array_size": 2,
          "map_offset": 2,
          "name": "record_1[0].record_1[1]",
          "read_permission": [
            0
          ],
          "readable": false,
          "resolved_access": 0,
          "resolved_array_size": 2,
          "resolved_offset": 0,
          "resolved_read_permission": 0,
          "resolved_total_size": 4,
          "resolved_type": "uint16_t",
          "resolved_type_size": 2,
          "resolved_write_permission": 0,
          "type": "uint16_t",
          "use_bitfields": false,
          "use_defines": false,
          "use_enums": false,
          "writable": false,
          "write_permission": [
            0
          ]
        },
        {
          "array_size": 2,
          "map_offset": 4,
          "name": "record_1[1].record_1[0]",
          "read_permission": [
            0
          ],
          "readable": false,
          "resolved_access": 0,
          "resolved_array_size": 2,
          "resolved_offset": 0,
          "resolved_read_permission": 0,
          "resolved_total_size": 4,
          "resolved_type": "uint16_t",
          "resolved_type_size": 2,
          "resolved_write_permission": 0,
          "type": "uint16_t",
          "use_bitfields": false,
          "use_defines": false,
          "use_enums": false,
          "writable": false,
          "write_permission": [
            0
          ]
        },
        {
          "array_size": 2,
          "map_offset": 6,
          "name": "record_1[1].record_1[1]",
          "read_permission": [
            0
          ],
          "readable": false,
          "resolved_access": 0,
          "resolved_array_size": 2,
          "resolved_offset": 0,
          "resolved_read_permission": 0,
          "resolved_total_size": 4,
          "resolved_type": "uint16_t",
          "resolved_type_size": 2,
          "resolved_write_permission": 0,
          "type": "uint16_t",
          "use_bitfields": false,
          "use_defines": false,
          "use_enums": false,
          "writable": false,
          "write_permission": [
            0
          ]
        },
        {
          "array_size": 2,
          "map_offset": 8,
          "name": "record_1[2].record_1[0]",
          "read_permission": [
            0
          ],
          "readable": false,
          "resolved_access": 0,
          "resolved_array_size": 2,
          "resolved_offset": 0,
          "resolved_read_permission": 0,
          "resolved_total_size": 4,
          "resolved_type": "uint16_t",
          "resolved_type_size": 2,
          "resolved_write_permission": 0,
          "type": "uint16_t",
          "use_bitfields": false,
          "use_defines": false,
          "use_enums": false,
          "writable": false,
          "write_permission": [
            0
          ]
        },
        {
          "array_size": 2,
          "map_offset": 10,
          "name": "record_1[2].record_1[1]",
          "read_permission": [
            0
          ],
          "readable": false,
          "resolved_access": 0,
          "resolved_array_size": 2,
          "resolved_offset": 0,
          "resolved_read_permission": 0,
          "resolved_total_size": 4,
          "resolved_type": "uint16_t",
          "resolved_type_size": 2,
          "resolved_write_permission": 0,
          "type": "uint16_t",
          "use_bitfields": false,
          "use_defines": false,
          "use_enums": false,
          "writable": false,
          "write_permission": [
            0
          ]
        }
      ],
      "type": "type_5"
    }
  },
  "metadata": {
    "app_name": "simple_full",
    "default_map": "map_3",
    "full_hash": "34acaa75f040a9dfb214ce13bc8b8cb0",
    "fw_hash": "4682bc472748f4914b0c8695ef177cb2",
    "major_version": 0,
    "minor_version": 0,
    "patch_version": 0,
    "permission_users": [
      "user",
      "other"
    ],
    "resolved_permission_users": {
      "other": 2,
      "user": 1
    },
    "sw_hash": "ab6b02d2e6f98ba152504942bba93e5e",
    "version": "0.0.0"
  },
  "typedefs": [
    {
      "type_2": {
        "deps": [],
        "elements": [
          {
            "name": "record_1",
            "resolved_offset": 0,
            "resolved_total_size": 4,
            "resolved_type": "uint32_t",
            "resolved_type_size": 4
          }
        ],
        "resolved_total_size": 4,
        "use_bitfields": false,
        "use_defines": false,
        "use_enums": false
      }
    },
    {
      "type_4": {
        "deps": [],
        "elements": [
          {
            "array_size": 2,
            "name": "record_1",
            "resolved_array_size": 2,
            "resolved_offset": 0,
            "resolved_total_size": 4,
            "resolved_type": "uint16_t",
            "resolved_type_size": 2,
            "type": "uint16_t"
          }
        ],
        "resolved_total_size": 4,
        "use_bitfields": false,
        "use_defines": false,
        "use_enums": false
      }
    },
    {
      "type_5": {
        "deps": [
          "type_4",
          "type_5"
        ],
        "elements": [
          {
            "array_size": 3,
            "name": "record_1",
            "resolved_array_size": 3,
            "resolved_offset": 0,
            "resolved_total_size": 12,
            "resolved_type": "type_4",
            "resolved_type_size": 4,
            "type": "type_4"
          }
        ],
        "read_permission": 0,
        "resolved_total_size": 12,
        "use_bitfields": false,
        "use_defines": false,
        "use_enums": false,
        "write_permission": 0
      }
    },
    {
      "type_1": {
        "deps": [
          "type_2",
          "type_1"
        ],
        "elements": [
          {
            "default": 1,
            "name": "record_1",
            "read_permission": "user",
            "resolved_offset": 0,
            "resolved_total_size": 4,
            "resolved_type": "uint32_t",
            "resolved_type_size": 4,
            "type": "uint32_t",
            "write_permission": "user"
          },
          {
            "array_size": 2,
            "default": 2,
            "name": "record_2",
            "read_permission": "user",
            "resolved_array_size": 2,
            "resolved_offset": 4,
            "resolved_total_size": 4,
            "resolved_type": "uint16_t",
            "resolved_type_size": 2,
            "type": "uint16_t"
          },
          {
            "array_size": "def_1",
            "default": "def_1",
            "name": "record_3",
            "resolved_array_size": 3,
            "resolved_offset": 8,
            "resolved_total_size": 3,
            "resolved_type": "uint8_t",
            "resolved_type_size": 1,
            "type": "uint8_t",
            "write_permission": "user"
          },
          {
            "name": "record_4",
            "resolved_offset": 11,
            "resolved_total_size": 1,
            "resolved_type": "bf_1",
            "resolved_type_size": 1,
            "type": "bf_1"
          },
          {
            "array_size": 1,
            "name": "record_5",
            "resolved_array_size": 1,
            "resolved_offset": 12,
            "resolved_total_size": 1,
            "resolved_type": "bf_1",
            "resolved_type_size": 1,
            "type": "bf_1"
          },
          {
            "array_size": "def_1",
            "name": "record_6",
            "resolved_array_size": 3,
            "resolved_offset": 13,
            "resolved_total_size": 6,
            "resolved_type": "bf_2",
            "resolved_type_size": 2,
            "type": "bf_2"
          },
          {
            "name": "record_7",
            "resolved_offset": 19,
            "resolved_total_size": 4,
            "resolved_type": "type_2",
            "resolved_type_size": 4,
            "type": "type_2"
          },
          {
            "array_size": 4,
            "name": "record_8",
            "resolved_array_size": 4,
            "resolved_offset": 23,
            "resolved_total_size": 16,
            "resolved_type": "type_2",
            "resolved_type_size": 4,
            "type": "type_2"
          },
          {
            "array_size": "def_1",
            "name": "record_9",
            "resolved_array_size": 3,
            "resolved_offset": 39,
            "resolved_total_size": 12,
            "resolved_type": "type_2",
            "resolved_type_size": 4,
            "type": "type_2"
          }
        ],
        "read_permission": 0,
        "resolved_total_size": 51,
        "use_bitfields": true,
        "use_defines": true,
        "use_enums": false,
        "write_permission": 0
      }
    },
    {
      "type_3": {
        "deps": [
          "type_1",
          "type_3"
        ],
        "elements": [
          {
            "array_size": 2,
            "name": "record_1",
            "resolved_array_size": 2,
            "resolved_offset": 0,
            "resolved_total_size": 102,
            "resolved_type": "type_1",
            "resolved_type_size": 51,
            "type": "type_1"
          }
        ],
        "read_permission": 0,
        "resolved_total_size": 102,
        "use_bitfields": false,
        "use_defines": false,
        "use_enums": false,
        "write_permission": 0
      }
    }
  ]
}"""
    return json.loads(json_cfg)


@pytest.fixture
def map_minimal():
    json_cfg = """{
  "bitfields": {},
  "defines": {},
  "enums": {},
  "maps": {
    "map_1": {
      "compressed_records": [
        {
          "compressed_offset": "0",
          "map_offset": 0,
          "name": "record_1",
          "read_permission": [
            0
          ],
          "readable": false,
          "resolved_access": 0,
          "resolved_offset": 0,
          "resolved_read_permission": 0,
          "resolved_total_size": 4,
          "resolved_type": "uint32_t",
          "resolved_type_size": 4,
          "resolved_write_permission": 0,
          "use_bitfields": false,
          "use_enums": false,
          "writable": false,
          "write_permission": [
            0
          ]
        }
      ],
      "records": [
        {
          "map_offset": 0,
          "name": "record_1",
          "read_permission": [
            0
          ],
          "readable": false,
          "resolved_access": 0,
          "resolved_offset": 0,
          "resolved_read_permission": 0,
          "resolved_total_size": 4,
          "resolved_type": "uint32_t",
          "resolved_type_size": 4,
          "resolved_write_permission": 0,
          "use_bitfields": false,
          "use_enums": false,
          "writable": false,
          "write_permission": [
            0
          ]
        }
      ],
      "type": "type_1"
    }
  },
  "metadata": {
    "app_name": "minimal",
    "full_hash": "ebd53a3f636abf35c32d076c513b2ae3",
    "fw_hash": "ad00a6ae13fdcb8dcc2fed692ad4548f",
    "major_version": 0,
    "minor_version": 0,
    "patch_version": 0,
    "resolved_permission_users": {},
    "sw_hash": "ad00a6ae13fdcb8dcc2fed692ad4548f",
    "version": "0.0.0"
  },
  "typedefs": [
    {
      "type_1": {
        "deps": [
          "type_1"
        ],
        "elements": [
          {
            "name": "record_1",
            "resolved_offset": 0,
            "resolved_total_size": 4,
            "resolved_type": "uint32_t",
            "resolved_type_size": 4
          }
        ],
        "read_permission": 0,
        "resolved_total_size": 4,
        "use_bitfields": false,
        "use_enums": false,
        "write_permission": 0
      }
    }
  ]
}"""
    return json.loads(json_cfg)


def test_gen_minimal(regtest, map_minimal):
    input_data = {'generated_maps': {'map_1': {'type': 'type_1'}},
                  'metadata': {'app_name': 'minimal'},
                  'typedefs': {'type_1': {'elements': ['record_1']}}}
    gen = MMMExporter(mm_cfg=map_minimal,
                      mm_input_data=input_data,
                      hide_version=True)
    for fname, data in gen.gen_cfg_files().items():
        regtest.write(f'file {fname}\n')
        regtest.write(data)
        regtest.write('\n')
    for fname, data in gen.gen_csv_files().items():
        regtest.write(f'file {fname}\n')
        regtest.write(data)
        regtest.write('\n')
    c_files = gen.gen_c_files()
    assert "Generated from the memory map manager version" not in c_files['mm_cc.h']
    for fname, data in c_files.items():
        regtest.write(f'file {fname}\n')
        regtest.write(data)
        regtest.write('\n')


def test_gen_full_simple(map_simple_full):
    """Simply generate a full map.

    As this is too much to review we just use it to check no exceptions.
    """
    gen = MMMExporter(mm_cfg=map_simple_full, mm_input_data={})
    c_files = gen.gen_c_files()
    assert len(gen.gen_cfg_files()) > 0
    assert len(gen.gen_c_files()) > 0
    assert len(gen.gen_csv_files()) > 0
    assert "Generated from the memory map manager version" in c_files['mm_cc.h']
