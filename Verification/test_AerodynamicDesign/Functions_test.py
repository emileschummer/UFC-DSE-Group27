import sys
import os

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

def test_FA_1(tmp_path):
    #test_load_airfoil_dat
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
    # Only lines with two valid floats should remain
    expected = np.array([
        [1.0, 0.0],
        [2.0, 1.0],
        [5.0, 3.0],
    ])
    assert isinstance(arr, np.ndarray)
    assert arr.dtype == float
    assert arr.shape == expected.shape
    np.testing.assert_allclose(arr, expected)


def test_FA_2():
    #test_wing_geometry_calculator
    InputWeight = 1000.0  # [N]
    velocity_op = 50.0  # [m/s]
    altitude = 0.0  # [m]
    taper_ratio = 0.5
    b = 10.0  # [m]

    S, cr, ct = wing_geometry_calculator(InputWeight, aero_df, velocity_op, altitude, taper_ratio, b)

    assert isinstance(S, float)
    assert isinstance(cr, float)
    assert isinstance(ct, float)
    def test_FA_2():
        #test_wing_geometry_calculator

        InputWeight = 1000.0  # [N]
        velocity_op = 50.0  # [m/s]
        altitude = 0.0  # [m] 
        taper_ratio = 0.5
        b = 10.0  # [m]


        S_actual, cr_actual, ct_actual = wing_geometry_calculator(InputWeight, aero_df, velocity_op, altitude, taper_ratio, b)

        assert isinstance(S_actual, float)
        assert isinstance(cr_actual, float)
        assert isinstance(ct_actual, float)

        max_idx = aero_df["CL_corrected"].idxmax()
        target_idx = max_idx - 3 if max_idx - 3 >= 0 else max_idx
        CL_expected_from_df = aero_df["CL_corrected"].iloc[target_idx]

        op_point_for_atmo = asb.OperatingPoint(velocity=velocity_op, atmosphere=asb.Atmosphere(altitude=altitude))
        rho_expected = op_point_for_atmo.atmosphere.density()

        S_expected = InputWeight / (0.5 * rho_expected * velocity_op**2 * CL_expected_from_df)
        cr_expected = 4 * S_expected / (b * (1 + taper_ratio))
        ct_expected = cr_expected * taper_ratio

        np.testing.assert_allclose(S_actual, S_expected, rtol=1*10**-5)
        np.testing.assert_allclose(cr_actual, cr_expected, rtol=1*10**-5)
        np.testing.assert_allclose(ct_actual, ct_expected, rtol=1*10**-5)

  
        altitude_high = 10000.0 # [m]
        S_high_alt, cr_high_alt, ct_high_alt = wing_geometry_calculator(InputWeight, aero_df, velocity_op, altitude_high, taper_ratio, b)
        
        op_point_high_alt = asb.OperatingPoint(velocity=velocity_op, atmosphere=asb.Atmosphere(altitude=altitude_high))
        rho_high_alt = op_point_high_alt.atmosphere.density()

        S_expected_high_alt = InputWeight / (0.5 * rho_high_alt * velocity_op**2 * CL_expected_from_df) 
        cr_expected_high_alt = 4 * S_expected_high_alt / (b * (1 + taper_ratio))
        ct_expected_high_alt = cr_expected_high_alt * taper_ratio

        np.testing.assert_allclose(S_high_alt, S_expected_high_alt, rtol=1e-5)
        assert S_high_alt > S_actual # Expect larger wing area at higher altitude
        np.testing.assert_allclose(cr_high_alt, cr_expected_high_alt, rtol=1e-5)
        np.testing.assert_allclose(ct_high_alt, ct_expected_high_alt, rtol=1e-5)


