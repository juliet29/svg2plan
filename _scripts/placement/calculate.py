from decimal import Decimal
from domains.domain import Domain

def calculate_domain_differences(domain: Domain):
    x_min, x_max, y_min, y_max = domain.get_values()
    dif_x = abs(x_max - x_min)
    dif_y = abs(y_max - y_min)
    return dif_x, dif_y

def create_new_domain(domain: Domain, new_x_left: Decimal, new_y_top: Decimal):
    dif_x, dif_y = calculate_domain_differences(domain)
    new_x_max = dif_x + new_x_left
    new_y_min = new_y_top - dif_y

    return Domain.create_domain(
            [new_x_left, new_x_max, new_y_min, new_y_top], domain.name
        )

def place_north_west(domain: Domain):
    new_x_left = Decimal(0)
    new_y_top = Decimal(0)
    return create_new_domain(domain, new_x_left, new_y_top)


def place_east(domain: Domain, west_domain: Domain):
    new_x_left = west_domain.x.max
    new_y_top = Decimal(0)
    return create_new_domain(domain, new_x_left, new_y_top)

def place_south(domain: Domain, north_domain: Domain):
    new_x_left = Decimal(0)
    new_y_top = north_domain.y.min
    return create_new_domain(domain, new_x_left, new_y_top)


def place_south_east(domain: Domain, north_domain: Domain, new_x_domain: Domain):
    new_x_left = new_x_domain.x.min
    new_y_top = north_domain.y.min
    return create_new_domain(domain, new_x_left, new_y_top)

