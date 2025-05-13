import sys
import os

# Add the parent directory of 'Battery_Modelling' to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import pytest as pt
import numpy as np
from Battery_Modelling.Modelling.UFC_MMA_4_Yangda import calculate_power_UFC_MMA_4

# Test parameters
CD0 = 0.0264 #same as osprey
piAe = 20.41 #same as osprey
S = 1.25 #m^2 x2.5 compared to research (cuz reearch is 10kg, we go 25)
W = 250 #N
CLmax = 1.3824 *0.9 #same as osprey


r=0.21 #same as osprey
A = np.pi*(r**2) #m^2
eta = 0.8
prop_efficiency = 0.8
numberengines_vertical = 4
numberengines_horizontal = 1
Avertical = A #individual propellor
Ahorizontal = A #individual propellor

expected_power1 = 4684.318879 
expected_power2 = 5559.07328
expected_power3 = 2223.885087

def test_calculate_power_UFC_MMA_4():
   
    
    # Call the function with the test input
    result1 = calculate_power_UFC_MMA_4(np.pi/9, 10, 1.225)
    result2 = calculate_power_UFC_MMA_4(np.pi/9, 0, 1.225)
    result3 = calculate_power_UFC_MMA_4(np.pi/9, 20, 1.225)

    # Assert that the result is close to the expected value
    assert pt.approx(result1, rel=1e-1) == expected_power1
    assert pt.approx(result2, rel=1e-1) == expected_power2
    assert pt.approx(result3, rel=1e-1) == expected_power3