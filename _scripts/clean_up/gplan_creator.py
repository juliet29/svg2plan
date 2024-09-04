from typing import TypedDict, Optional, Dict
from svg_helpers.domains import Corners
import os
import json


class GPLANRoomType(TypedDict):
    label: str
    left: float
    top: float
    width: float
    height: float
    id: Optional[float] 
    color: Optional[str] 


# final json format is [[{obj}, {obj}...]]


class GPLANCreator:
    def __init__(self, corners: Dict[str, Corners]) -> None:
        self.corners = corners
        self.rooms = []
        self.plan = []
        # self.file_name = file_name

    def run(self):
        self.create_rooms()
        self.write_to_file()

    def create_rooms(self):
        for ix, (room, data) in enumerate(self.corners.items()):
            width = abs(data.x_right - data.x_left)
            height = abs(data.y_top - data.y_bottom)
            data.y_top*=-1 # flipped in y direction -> distance from top
            g_room: GPLANRoomType = {
                "id": ix,
                "label": room,
                "left": data.x_left,
                "top": data.y_top,
                "width": width,
                "height": height,
                "color": ""
            }
            self.rooms.append(g_room)
        self.plan.append(self.rooms)

    def write_to_file(self):
        path = os.path.join("../outputs", "amber_a", "gplan.json")
        with open(path, 'w+') as file:
            json.dump(self.plan, default=str, fp=file)


