from dataclasses import dataclass
from shapely import LineString, STRtree, union_all, Polygon
from svg_helpers.layout import Layout
from svg_helpers.directions import Direction, make_directed_pairEW
from svg_helpers.layout_base import LayoutBase
from problems.classes.problem import Problem, ProblemType
from log_setter.log_settings import svlogger

SIDE_HOLE_PAIRS = {
    Direction.NORTH: [Direction.EAST, Direction.WEST],
    Direction.SOUTH: [Direction.EAST, Direction.WEST],
    Direction.EAST: [Direction.NORTH, Direction.SOUTH],
    Direction.WEST: [Direction.NORTH, Direction.SOUTH],
}


@dataclass
class SideHoleData:
    pair: list
    geometry: Polygon
    direction: Direction


class SideHoleIdentifier(LayoutBase):
    def __init__(self, layout: Layout) -> None:
        super().__init__(layout)
        self.problems: list[Problem] = []
        self.side_hole_pairs: list[SideHoleData] = []
        self.possible_pairs: list[list] = []
        self.unique_pairs: set

    def report_problems(self):
        # try:
        self.find_potential_holes()
        # except AttributeError:
        #     return self.shapes

        self.search_layout()
        for ix, pair in enumerate(self.side_hole_pairs):
            self.problems.append(
                Problem(
                    ix,
                    ProblemType.SIDE_HOLE,
                    nbs=pair.pair,
                    direction=pair.direction,
                    geometry=pair.geometry,
                )
            )

    def find_potential_holes(self):
        shapes = list(self.shapes.values())
        union = union_all(shapes)
        diffs = union.convex_hull.difference(union)
        try:
            self.tree = STRtree(diffs.geoms)  # type: ignore
        except AttributeError:
            svlogger.warning(diffs)
            raise AttributeError("error getting side hole holes")

    def search_layout(self):
        for dir in Direction:
            self.direction = dir
            for node, data in self.G.nodes(data=True):
                if not data["data"][dir.name]:
                    self.node = node
                    self.node_data = data["data"]
                    self.find_nonadjacent_nbs()
        self.clean_up_nbs()

    # TODO => make this clearer => is_on_facade()

    def find_nonadjacent_nbs(self):
        nbs = self.find_nbs_in_direction()
        for nb in nbs:
            if not self.shapes[self.node].touches(self.shapes[nb]):
                if not self.shapes[self.node].overlaps(self.shapes[nb]):
                    self.possible_pairs.append([self.node, nb])

    def find_nbs_in_direction(self):
        dir1, dir2 = SIDE_HOLE_PAIRS[self.direction]
        nbs = self.node_data[dir1.name] + self.node_data[dir2.name]
        true_nbs = [n for n in nbs if not self.G.nodes[n]["data"][self.direction.name]]
        return true_nbs

    def clean_up_nbs(self):
        self.filter_nbs()
        for pair in self.unique_pairs:
            self.pair = pair
            if self.is_pair_EW():
                self.find_pair_geom()
                shp = SideHoleData(list(pair), self.geom, self.direction)
                self.side_hole_pairs.append(shp)

    def filter_nbs(self):
        pairs = [frozenset(p) for p in self.possible_pairs]
        self.unique_pairs = set(pairs)

    def is_pair_EW(self):
        self.EW_pair = make_directed_pairEW(self.G, *self.pair)
        try:
            assert self.EW_pair
            return True
        except:
            svlogger.debug("This is not an EW side hole")
            return False

    def find_pair_geom(self):
        self.create_test_line()
        ix = self.tree.nearest(self.test_line)
        self.geom = Polygon(self.tree.geometries.take(ix))

    def create_test_line(self):
        assert self.EW_pair
        y = self.shapes[self.EW_pair.WEST].centroid.y
        x_right = self.domains[self.EW_pair.WEST].x.max
        x_left = self.domains[self.EW_pair.EAST].x.min
        self.test_line = LineString([[x_right, y], [x_left, y]])
