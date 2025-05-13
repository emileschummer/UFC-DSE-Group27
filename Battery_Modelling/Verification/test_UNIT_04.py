import sys
import os

# Add the parent directory of 'Battery_Modelling' to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import pytest as pt
import numpy as np
from Battery_Modelling.Modelling.UFC_MMA_3_Osprey import calculate_power_UFC_MMA_3

# Test parameters
CD0 = 0.0264 #https://www.researchgate.net/publication/351569758_Conceptual_design_of_a_fixed_wing_vertical_take-off_and_landing_unmanned_aerial_vehicle
piAe = 20.41 #https://www.researchgate.net/publication/351569758_Conceptual_design_of_a_fixed_wing_vertical_take-off_and_landing_unmanned_aerial_vehicle

S = 1.25 #m^2 x2.5 compared to research (cuz reearch is 10kg, we go 25)
W = 250 #N
CLmax = 1.3824 *0.9 #https://www.researchgate.net/publication/351569758_Conceptual_design_of_a_fixed_wing_vertical_take-off_and_landing_unmanned_aerial_vehicle
#clmax is 2 says: https://www.sciencedirect.com/science/article/pii/S2090447922004051



r=0.21 #https://www.researchgate.net/publication/351569758_Conceptual_design_of_a_fixed_wing_vertical_take-off_and_landing_unmanned_aerial_vehicle
A = np.pi*(r**2) #m^2
eta = 0.8 
numberengines = 2
expected_power1 = 4592.550332 
expected_power2 = 5996.913091
expected_power3 = 1572.503012

def test_calculate_power_UFC_MMA_3():
    """
    Test the calculate_power_UFC_MMA_1 function.
    """
    
    # Call the function with the test input
    result1 = calculate_power_UFC_MMA_3(np.pi/9, 10, 1.225)
    result2 = calculate_power_UFC_MMA_3(np.pi/9, 0, 1.225)
    result3 = calculate_power_UFC_MMA_3(np.pi/9, 20, 1.225)

    # Assert that the result is close to the expected value
    assert pt.approx(result1, rel=1e-1) == expected_power1
    assert pt.approx(result2, rel=1e-1) == expected_power2
    assert pt.approx(result3, rel=1e-1) == expected_power3