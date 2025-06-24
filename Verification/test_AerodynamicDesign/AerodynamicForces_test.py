import sys
import os
import pytest
import numpy as np
from unittest.mock import MagicMock, patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from Final_UAV_Sizing.Modelling.Wing_Sizing.AerodynamicForces import load_distribution_halfspan

# Mock object to represent a wing cross-section
class MockXSec:
    def __init__(self, xyz_le):
        self.xyz_le = xyz_le

@pytest.fixture
def mock_wing_geom():
    """Create a mock wing geometry with 5 cross sections."""
    xsecs = [MockXSec([0, y, 0]) for y in np.linspace(0, 2.0, 5)] #y = 0, 0.5, 1.0, 1.5, 2.0
    wing = MagicMock()
    wing.xsecs = xsecs
    return wing

@pytest.fixture
def mock_lift_distribution():
    """Provide a sample lift distribution for different alphas."""
    return {
        "alpha": [0, 5, 10],
        "CLs": [
            [0.1, 0.2, 0.3, 0.4],  # For alpha=0
            [0.5, 0.6, 0.7, 0.8],  # For alpha=5
            [0.9, 1.0, 1.1, 1.2]   # For alpha=10
        ] #one per pannel between points
    }

#######################################################################################
#######################################################################################
#######################################################################################

                        # TESTING #


#######################################################################################
#######################################################################################
#######################################################################################


@patch('Final_UAV_Sizing.Modelling.Wing_Sizing.AerodynamicForces.plt')
def test_AF_1(mock_plt, mock_wing_geom, mock_lift_distribution):
    #test_load_distribution_calculation
    """
    Test if function correctly calculates normalized spanwise locations
    and return correct data structure for specific alpha.
    """
    alpha_to_test = 5
    half_span = 2.0  # Corresponds to the full span of the mock wing

    
    distribution = load_distribution_halfspan(
        wing_geom=mock_wing_geom,
        lift_distribution=mock_lift_distribution,
        alpha=alpha_to_test,
        half_span=half_span,
        plot=False  
    )

    expected_div = np.array([0.125, 0.375, 0.625, 0.875])

    # Expected CLs for alpha=5 from mock distribution
    expected_cls = [0.5, 0.6, 0.7, 0.8]

    # Check structure
    assert isinstance(distribution, list)
    assert len(distribution) == 2

    # Check the calculated values
    np.testing.assert_allclose(distribution[0], expected_div, rtol=1e-6)
    assert distribution[1] == expected_cls

