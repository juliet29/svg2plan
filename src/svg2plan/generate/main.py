from random import randrange, randint, seed
import shapely

from svg2plan.visuals.plots import subplot_layout
from ..domains.domain import Domain, Coordinate, get_domains_extents
from ..helpers.shapely import domains_to_shape
from ..helpers.utils import float_to_decimal
from plotly.subplots import make_subplots


def pick_n_domains(lims=(3, 5)) -> int:
    return randint(*lims)


def pick_dimension(lims=(1, 8)):
    return float_to_decimal(randrange(*lims))


def pick_distance(lims=(0, 2)):
    return float_to_decimal(randrange(*lims))


def pick_position(domains: list[Domain]):
    last = domains[-1]
    new_x = last.x.max + pick_distance()
    new_y = last.x.max + pick_distance()
    return Coordinate(new_x, new_y)
    # shape = domains_to_shape(domains)
    # convex_ext = shapely.get_exterior_ring(shape)


def generate_domains():
    seed(0)
    domains: list[Domain] = []
    n_domains = pick_n_domains()

    def create_new_domain(ix):
        if ix == 0:
            coord = Coordinate.create_coordinate(0, 0)
        else:
            coord = pick_position(domains)

        x_size = pick_dimension()
        y_size = pick_dimension()

        new_domain = Domain.create_domain_from_coordinate(
            coord, x_size, y_size, str(ix)
        )

        return new_domain

    for ix in range(n_domains):
        domains.append(create_new_domain(ix))

    return domains


def plot_domains(domains: list[Domain]):
    extent = get_domains_extents(domains)
    fig = make_subplots(rows=1, cols=1)
    return subplot_layout(
        fig,
        domains,
        1,
        1,
        label="test",
        xrange=extent.x.as_list,
        yrange=extent.y.as_list,
        label_shapes=True
    )
