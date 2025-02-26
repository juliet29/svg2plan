# from svg2plan.domains.domain import Domain
# from domains.range import nonDecimalRange
import pytest
from svg2plan.domains.range import nonDecimalRange
from svg2plan.domains.domain import Domain


@pytest.fixture()
def control():
    return nonDecimalRange(10, 20).toRange()

@pytest.fixture
def larger():
    return nonDecimalRange(21, 23).toRange()

@pytest.fixture
def smaller():
    return nonDecimalRange(6, 7.5).toRange()


@pytest.fixture
def north_domain(control, larger):
    return Domain(name="north", x=control, y=larger)

@pytest.fixture
def south_domain(control, smaller):
    return Domain(name="south", x=control, y=smaller)

@pytest.fixture
def east_domain(control, larger):
    return Domain(name="east", x=larger, y=control)

@pytest.fixture
def west_domain(control, smaller):
    return Domain(name="west", x=smaller, y=control)

@pytest.fixture
def east_north_domain(larger):
    return Domain(name="en", x=larger, y=larger)

@pytest.fixture
def west_south_domain(smaller):
    return Domain(name="ws", x=smaller, y=smaller)