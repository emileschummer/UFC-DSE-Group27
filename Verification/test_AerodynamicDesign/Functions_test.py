import sys
import os

# Add the parent directory of 'Acceleration_try' to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))




import numpy as np
import pytest as pt
import pandas as pd
from Final_UAV_Sizing.Modelling.Wing_Sizing.Functions import *
from Final_UAV_Sizing.Input.fixed_input_values import *
aero_df= pd.read_csv(aero_csv)

#######################################################################################
#######################################################################################
#######################################################################################

                        # TESTING #


#######################################################################################
#######################################################################################
#######################################################################################

def test_load_airfoil_dat(tmp_path):
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
    assert isinstance(arr, np.ndarray)
    assert arr.dtype == float
    assert arr.shape == expected.shape
    np.testing.assert_allclose(arr, expected)


def test_wing_geometry_calculator():
    # Test with a simple case
    InputWeight = 1000.0  # N
    velocity_op = 50.0  # m/s
    altitude = 0.0  # m
    taper_ratio = 0.5
    b = 10.0  # m

    S, cr, ct = wing_geometry_calculator(InputWeight, aero_df, velocity_op, altitude, taper_ratio, b)

    assert isinstance(S, float)
    assert isinstance(cr, float)
    assert isinstance(ct, float)