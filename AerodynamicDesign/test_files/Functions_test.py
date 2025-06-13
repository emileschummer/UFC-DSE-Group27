import numpy as np
import pytest
from Functions import load_airfoil_dat, wing_geometry_calculator

@pytest.fixture
def airfoil_dat_file(tmp_path):
    content = """\
1.00000  0.00000
 0.66667  0.05000
 0.33333  0.05000
 0.00000  0.00000
 0.33333 -0.05000
 0.66667 -0.05000
 1.00000  0.00000
"""
    p = tmp_path / "test.dat"
    p.write_text(content)
    return str(p)

#######################################################################################
#######################################################################################
#######################################################################################

                        # TESTING #


#######################################################################################
#######################################################################################
#######################################################################################

def test_load_airfoil_dat_shape_and_dtype(airfoil_dat_file):
    arr = load_airfoil_dat(airfoil_dat_file)
    assert isinstance(arr, np.ndarray)
    assert arr.shape == (7, 2)
    assert arr.dtype == float

def test_load_airfoil_dat_values(airfoil_dat_file):
    arr = load_airfoil_dat(airfoil_dat_file)
    expected = np.array([
        [1.00000,  0.00000],
        [0.66667,  0.05000],
        [0.33333,  0.05000],
        [0.00000,  0.00000],
        [0.33333, -0.05000],
        [0.66667, -0.05000],
        [1.00000,  0.00000],
    ])
    np.testing.assert_allclose(arr, expected, rtol=1e-6, atol=1e-8)

def test_load_airfoil_dat_invalid_lines(tmp_path):
    content = """\
    1.0 0.0
    foo bar
    2.0 1.0
    3.0
    4.0 2.0 extra
    5.0 3.0
    """
    p = tmp_path / "mixed.dat"
    p.write_text(content)
    arr = load_airfoil_dat(str(p))
    # Only lines with exactly two valid floats should remain
    expected = np.array([
        [1.0, 0.0],
        [2.0, 1.0],
        [5.0, 3.0],
    ])
    assert arr.shape == expected.shape
    np.testing.assert_allclose(arr, expected)

def test_load_airfoil_dat_empty_file(tmp_path):
    p = tmp_path / "empty.dat"
    p.write_text("")
    arr = load_airfoil_dat(str(p))
    assert isinstance(arr, np.ndarray)
    assert arr.size == 0