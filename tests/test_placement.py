from svg2plan.domains.domain import Domain
from svg2plan.domains.range import nonDecimalRange
import pytest
from svg2plan.placement.attract import create_graph, adjust_domains
from svg2plan.placement.neighbors import get_possible_nbs, create_ranges_between
from svg2plan.svg_reader import SVGReader
from svg2plan.constants import BASE_PATH


x_max_root = 5
diff = 2
x_min_nb = x_max_root + diff


@pytest.fixture()
def root_domain():
    return Domain.create_domain([2, x_max_root, 0, 10], name="root_domain")


@pytest.fixture()
def nb_top():
    return Domain.create_domain([x_min_nb, 10, 7, 10], name="nb_top")


@pytest.fixture()
def nb_bottom():
    return Domain.create_domain([x_min_nb, 10, 0, 5], name="nb_bottom")


@pytest.fixture()
def not_nb_bottom():
    return Domain.create_domain([x_max_root-2, 10, 0, 5], name="not_nb_bottom")


def create_domains_dict(arr: list[Domain]):
    return {i.name: i for i in arr}

@pytest.fixture()
def domains():
    path = BASE_PATH / "tests" / "svgs" / "_05_rect.svg"
    sv = SVGReader(path)
    sv.run()
    return sv.domains



@pytest.mark.parametrize(
    "bottom_domain, expected",
    [("nb_bottom", [True, True]), ("not_nb_bottom", [True, False])],
)
def test_can_find_neighbors(
    root_domain: Domain,
    nb_top: Domain,
    bottom_domain,
    expected: tuple[bool, bool],
    request,
):
    _bottom_domain = request.getfixturevalue(bottom_domain)
    domains = create_domains_dict([root_domain, nb_top, _bottom_domain])
    poss_nbs = get_possible_nbs(root_domain, domains, ax="x")
    assert [nb_top in poss_nbs, _bottom_domain in poss_nbs] == expected


def test_create_range_between(root_domain: Domain, nb_top: Domain, nb_bottom: Domain):
    ranges = create_ranges_between(root_domain, [nb_top, nb_bottom], "x" )
    curr_range = nonDecimalRange(x_max_root, x_min_nb).toRange()
    expected_ranges = {nb_top.name: curr_range, nb_bottom.name: curr_range}
    assert ranges == expected_ranges




def test_graph_creation(domains):
    G = create_graph(domains, "x")
    assert ("A", "B") in G.edges
    assert ("A", "E") in G.edges
    assert ("A", "D") not in G.edges
    assert ("A", "C") not in G.edges


def test_can_attract_domains(domains):
    xy_domains, _ = adjust_domains(domains)
    assert xy_domains["A"]["x"].max == xy_domains["B"]["x"].min 
    assert xy_domains["B"]["x"].max == xy_domains["C"]["x"].min 
    assert xy_domains["D"]["y"].max == xy_domains["C"]["y"].min 
    
