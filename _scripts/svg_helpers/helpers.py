from typing import Dict,  Union
import json
from svg_helpers.domains import Corners

def print_hi():
    print("hi")



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


def get_bounds_of_layout(coordinates: Dict[str, tuple]):
        x_values = [coord[0] for coord in coordinates.values()]
        y_values = [coord[1] for coord in coordinates.values()]


        x_min = min(x_values)
        x_max = max(x_values)
        y_min = min(y_values)
        y_max = max(y_values)

        return Corners(x_min, x_max, y_min, y_max)