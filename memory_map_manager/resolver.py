import json
from pandas import DataFrame
import pandas as pd
import operator
PRIM_ENUM_LIST = ['uint8_t', 'int8_t', 'uint16_t', 'int16_t',
                  'uint32_t', 'int32_t', 'uint64_t', 'int64_t',
                  'char', 'float', 'double']

def _from_element(lods, key='type'):
    ret = []
    for ds in lods:
        ret.extend([x[key] for x in ds['elements']])
    return ret

def resolve_order(cfg):
    tds = {}
    # for td in cfg['typedefs']:
    #     if td['type_name'] not in resolved_types:
    #         for ele in td['elements']:
    #             if ele['type'] not in PRIM_ENUM_LIST:

    #         if all(ele['type'] in resolved_types for ele in td['elements']):


    tns = []
    tns.extend([x['type_name'] for x in cfg['typedefs']])
    tns.extend([x['type_name'] for x in cfg['bitfields']])
    ts = _from_element(cfg['typedefs'])
    print(tns, ts)

    tds = DataFrame(cfg['typedefs'])
    #print(DataFrame.from_records((tds['elements'][0]))['name'])
    #print(tds)
    typenames = tds['type_name', 'elements']
    print(typenames)
    #print(typenames)
    bfs = DataFrame(cfg['bitfields'])['type_name']
    #print(DataFrame(cfg['bitfields'])['type'])
    print(pd.concat([typenames, bfs]))




with open('/home/weiss/wd/memory_map_manager/example_typedef.json') as f:
    data = json.load(f)
df = pd.DataFrame([{'name':'a', 'type': 'ta'},
                   {'name':'a', 'type': 'tb'},
                   {'name':'a', 'type': 'c'},
                    {'name':'b', 'type': 'tb'},
                    {'name':'c', 'type': 'td'}])
print(df.to_dict())
#resolve_order(data)
