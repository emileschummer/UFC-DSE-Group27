import sys
import os

# Add the parent directory of 'Midterm_Battery_Modelling' to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import pytest as pt
import numpy as np
from Midterm_Battery_Modelling.Input.Configuration_inputs import *
from Midterm_Battery_Modelling.Modelling.UFC_MMA_3_Osprey import calculate_power_UFC_MMA_3

# Test parameters
inputs= [W, eta, CD0_MMA3, piAe_MMA3, S_MMA3, CLmax_MMA3, r_MMA3]

expected_power1 = 4592.550332 
expected_power2 = 5996.913091
expected_power3 = 1572.503012

def test_calculate_power_UFC_MMA_3():
  
    
    # Call the function with the test input
    result1 = calculate_power_UFC_MMA_3(np.pi/9, 10, 1.225, inputs)
    result2 = calculate_power_UFC_MMA_3(np.pi/9, 0, 1.225, inputs)
    result3 = calculate_power_UFC_MMA_3(np.pi/9, 20, 1.225, inputs)

    # Assert that the result is close to the expected value
    assert pt.approx(result1, rel=1e-1) == expected_power1
    assert pt.approx(result2, rel=1e-1) == expected_power2
    assert pt.approx(result3, rel=1e-1) == expected_power3