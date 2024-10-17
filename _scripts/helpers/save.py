from typing import Dict, TypedDict, Optional
from helpers.layout import DomainsDict
import pickle
from pathlib import Path


# final json format is [[{obj}, {obj}...]]
class RoomType(TypedDict):
    label: str
    left: str
    top: str
    width: str
    height: str
    id: Optional[float]
    color: Optional[str]


def create_plan(domains: DomainsDict) -> list[list[RoomType]]:
    rooms = []
    for ix, (room, data) in enumerate(domains.items()):
        width = float(abs(data.x.max - data.x.min))
        height = float(abs(data.y.max - data.y.min))
        g_room: RoomType = {
            "id": ix,
            "label": room,
            "left": str(data.x.min),
            "top": str(data.y.max),
            "width": str(width),
            "height": str(height),
            "color": "",
        }
        rooms.append(g_room)
    return [rooms]



def read_pickle(path:Path):
    with open(path, "rb") as handle:
        obj = pickle.load(handle)
    return obj

def write_pickle(path:Path, obj):
    with open(path, "wb") as handle:
        pickle.dump(obj, handle, protocol=pickle.HIGHEST_PROTOCOL)
    return path.name

def read_temp_sol(name):
    sols_path = Path.cwd().parent.parent / "temp_sols"
    path = sols_path / f"{name}.pickle"
    return read_pickle(path)

def write_temp_sol(name, obj):
    sols_path = Path.cwd().parent.parent / "temp_sols"
    path = sols_path / f"{name}.pickle"
    return write_pickle(path, obj)
