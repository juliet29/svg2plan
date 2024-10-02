from export.saver import read_pickle
from helpers.layout import Layout
from placement2.arrange import create_placement
import numpy as np


expected_placement_amber_c = np.array([['m_bed', 'bed1', '', ''],
       ['m_closet', 'transit', 'bed1_closet', ''],
       ['m_bath', 'corridor', 'linen', 'laundry'],
       ['bath', 'corridor', 'den', ''],
       ['kitchen', 'dining', 'den_closet', ''],
       ['living', '', '', '']], dtype=object) # type: ignore


def test_expected_placement():
    layout: Layout = read_pickle("1001_amber_c_ag")
    assert (expected_placement_amber_c == create_placement(layout)).all()