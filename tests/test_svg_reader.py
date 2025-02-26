import pytest
from pathlib import Path
from svg2plan.svg_reader import SVGReader
from svg2plan.constants import BASE_PATH




@pytest.mark.parametrize(
    "path", ["amber_a_f01.svg", "amber_b_f01.svg", "amber_c_f01.svg"]
)
def test_reading_valid_svgs(path: Path):
    sv = SVGReader(BASE_PATH / "svg_imports" / path)
    sv.run()
    assert len(sv.domains) > 3
    # TODO check that names and sizes match up, add more parameters.. 

# @pytest.mark.skip(reason="No invalid svgs quite yet...")
def test_reading_simple_svgs():
    sv = SVGReader(BASE_PATH / "tests" / "svgs" / "_05_rect.svg")
    sv.run()
    assert sv.domains

