import sys
import os

# Add the parent directory of 'Propeller_sizing' to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest as pt
from Final_UAV_Sizing.Input.RaceData.Strava_input_csv import *

#SI 1
h=1200
rho_hand= 1.089952589

def test_air_density_isa():
    """
    Test the air_density_isa function.
    """
    # Expected value for air density at 1200 m
    expected_rho = rho_hand

    # Call the function with the test input
    result = air_density_isa(h)

    # Assert that the result is close to the expected value
    assert pt.approx(result, rel=1e-6) == expected_rho

#SI 2
rho= 1.01
h_hand= 1965.22482011
def test_altitude_from_density():
    """
    Test the altitude_from_density function.
    """
    # Expected value for altitude from density
    expected_h = h_hand

    # Call the function with the test input
    result = altitude_from_density(rho)

    # Assert that the result is close to the expected value
    assert pt.approx(result, rel=1e-6) == expected_h

print(altitude_from_density(rho))
