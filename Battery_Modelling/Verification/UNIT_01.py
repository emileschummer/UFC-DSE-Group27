import pytest as pt
from Strava_input_csv import air_density_isa

h=1200

rho_hand= 1.090141083

def test_air_density_isa():
    """
    Test the air_density_isa function.
    """
    # Expected value for air density at 1200 m
    expected_rho = rho_hand

    # Call the function with the test input
    result = air_density_isa(h)

    # Assert that the result is close to the expected value
    assert pt.approx(result, rel=1e-5) == expected_rho

