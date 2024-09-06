from typing import Dict,  Union
import json

def key_from_value(dict:Dict, val):
    return list(dict.keys())[list(dict.values()).index(val)]

def compare_sequences(t1: Union[tuple, list], t2: Union[tuple, list]): 
    return sorted(t1) == sorted(t2)


def toJson(obj):
        return json.dumps(obj, default=lambda o: o.__dict__)