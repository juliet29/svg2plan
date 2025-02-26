from svg2plan.domains.domain import Domain


class TestDomain:
    def test_ns(self, north_domain, south_domain):
        res = north_domain.compare_domains(south_domain)
        assert res.NORTH == north_domain
        assert res.SOUTH == south_domain
        assert res.EAST == None
        assert res.WEST == None

    def test_ew(self, east_domain, west_domain):
        res = east_domain.compare_domains(west_domain)
        assert res.NORTH == None
        assert res.SOUTH == None
        assert res.EAST == east_domain
        assert res.WEST == west_domain

    def test_diagonal(self, east_north_domain, west_south_domain):
        res = east_north_domain.compare_domains(west_south_domain)
        assert res.NORTH == east_north_domain
        assert res.SOUTH == west_south_domain
        assert res.EAST == east_north_domain
        assert res.WEST == west_south_domain

    def test_get_other_axis(self, north_domain):
        assert north_domain.get_other_axis("y") == "x"

    def test_modification(self, north_domain):
        def fx(x):
            return x + 2
        res = north_domain.modify(fx)
        assert res.x.min == north_domain.x.min + 2
        assert res.y.max == north_domain.y.max + 2

    def test_creation(self):
        d = Domain.create_domain([1.1, 2.1, 3, 4])
        assert d.x.min.as_integer_ratio() == (11, 10)
        assert d.y.min.as_integer_ratio() == (3, 1)


# def check_contains(a,b):
#     print(f"a contains b: {a.contains(b)}")
#     print(f"b contains a: {b.contains(a)}")
# a = Range.create_range(10, 30)
# b = Range.create_range(8, 29)
# check_contains(a,b)
