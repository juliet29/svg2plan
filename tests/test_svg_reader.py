import pytest
from pathlib import Path
from svg2plan.svg_reader import SVGReader
from svg2plan.constants import BASE_PATH




@pytest.mark.parametrize(
    "path", ["amber_a_f01.svg", "amber_b_f01.svg", "amber_c_f01.svg", "_05_rect.svg"]
)
def test_reading_valid_svgs(path: Path):
    sv = SVGReader(BASE_PATH  / "tests" / "svgs" / path)
    sv.run()
    assert len(sv.domains) > 3
    # TODO check that names and sizes match up, add more parameters.. 
