from itertools import chain, groupby, tee
from typing import Any, Callable, Dict, Iterable, List, TypeVar, Union
import json


def key_from_value(dict: Dict, val):
    return list(dict.keys())[list(dict.values()).index(val)]


def indices(lst, val):
    return [i for i, x in enumerate(lst) if x == val]


def keys_from_value(dict: Dict, val):
    keys = list(dict.keys())
    vals = list(dict.values())
    ixes = indices(vals, val)
    return [keys[i] for i in ixes]


def compare_sequences(t1: Union[tuple, list], t2: Union[tuple, list]):
    return sorted(t1) == sorted(t2)


def toJson(obj):
    return json.dumps(obj, default=lambda o: o.__dict__)


def pairwise(iterable):
    """
    >>> xs = [0, 2, 4, 6, 8]
    >>> [i for i in pairwise(xs)]
    [(0, 2), (2, 4), (4, 6), (6, 8)]
    """
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


T = TypeVar("T")


def sort_and_group_objects(lst: List[T], fx: Callable[[T], Any]) -> List[List[T]]:
    sorted_objs = sorted(lst, key=fx)
    return [list(g) for _, g in groupby(sorted_objs, fx)]

# def sort_and_group_objects_with_keys(lst: List[T], fx: Callable[[T], Any]) -> List[tuple[Any, List[T]]]:
#     sorted_objs = sorted(lst, key=fx)
#     keys_and_groups: List[tuple[Any, Iterable[str]]] = []
#     for k, g in groupby(sorted_objs, key=fx):
#         group = list((i[0] for i in g))
#         keys_and_groups.append((key, group))


def chain_flatten(lst: Iterable[Iterable]):
    return list(chain.from_iterable(lst))
