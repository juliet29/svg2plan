from typing import Dict,  Union
import json

def key_from_value(dict:Dict, val):
    return list(dict.keys())[list(dict.values()).index(val)]

def indices(lst, val):
    return [i for i, x in enumerate(lst) if x == val]

def keys_from_value(dict:Dict, val):
    keys = list(dict.keys())
    vals = list(dict.values())
    ixes = indices(vals, val)
    return [keys[i] for i in ixes]

def compare_sequences(t1: Union[tuple, list], t2: Union[tuple, list]): 
    return sorted(t1) == sorted(t2)


def toJson(obj):
        return json.dumps(obj, default=lambda o: o.__dict__)