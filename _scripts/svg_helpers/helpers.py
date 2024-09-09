from typing import Dict,  Union
import json
from svg_helpers.domains import Corners

def key_from_value(dict:Dict, val):
    return list(dict.keys())[list(dict.values()).index(val)]

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