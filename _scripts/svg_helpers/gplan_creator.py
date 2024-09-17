import json
import os
from typing import Dict, TypedDict, Optional

from svg_helpers.domains import Corners, DecimalCorners


# final json format is [[{obj}, {obj}...]]

class GPLANRoomType(TypedDict):
    label: str
    left: str
    top: str
    width: str
    height: str
    id: Optional[float]
    color: Optional[str]


class GPLANCreator:
    def __init__(self, corners: Dict[str, DecimalCorners], folder:str = "amber_a") -> None:
        self.corners = corners
        self.rooms = []
        self.plan = []
        self.folder = folder

    def run(self):
        self.create_rooms()
        self.write_to_file()


    def create_rooms(self):
        for ix, (room, data) in enumerate(self.corners.items()):
            width = float(abs(data.x_right - data.x_left))
            height = float(abs(data.y_top - data.y_bottom))
            data.y_top *= -1  # flipped in y direction -> distance from top
            g_room: GPLANRoomType = {
                "id": ix,
                "label": room,
                "left": str(data.x_left),
                "top": str(data.y_top),
                "width": str(width),
                "height": str(height),
                "color": "",
            }
            self.rooms.append(g_room)
        self.plan.append(self.rooms)

    def write_to_file(self):
        name = "gplan.json" 
        path = os.path.join("../outputs", self.folder, name )
        with open(path, "w+") as file:
            json.dump(self.plan, default=str, fp=file)
