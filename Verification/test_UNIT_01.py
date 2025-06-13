import sys
import os

# Add the parent directory of 'Acceleration_try' to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest as pt
from Acceleration_try.Input.Strava_input_csv import air_density_isa

#Test parameters
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
    assert pt.approx(result, rel=1e-1) == expected_rho

