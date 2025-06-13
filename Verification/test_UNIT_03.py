import sys
import os

# Add the parent directory of 'Midterm_Battery_Modelling' to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import pytest as pt
import numpy as np
from Midterm_Battery_Modelling.Input.Configuration_inputs import *
from Midterm_Battery_Modelling.Modelling.UFC_MMA_1_Helicopter import calculate_power_UFC_MMA_1

# Test parameters
inputs= [W, eta, CD_MMA1, S_MMA1, A_MMA1]



expected_power= 3428.961415 # Expected value for power (to be calculated based on the formula)

def test_calculate_power_UFC_MMA_1():
   
    
    # Call the function with the test input
    result = calculate_power_UFC_MMA_1(np.pi/9, 10, 1.225, inputs)

    # Assert that the result is close to the expected value
    assert pt.approx(result, rel=1e-1) == expected_power

