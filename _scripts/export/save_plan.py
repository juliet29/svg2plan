from typing import Dict, TypedDict, Optional
from helpers.layout import DomainsDict


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
