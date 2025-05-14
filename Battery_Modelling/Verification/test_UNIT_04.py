import sys
import os

# Add the parent directory of 'Battery_Modelling' to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import pytest as pt
import numpy as np
from Battery_Modelling.Input.Configuration_inputs import *
from Battery_Modelling.Modelling.UFC_MMA_2_Quad import calculate_power_UFC_MMA_2

# Test parameters
inputs= [W, eta, CD_MMA2, Stop_MMA2, Sfront_MMA2, totalA_MMA2]
expected_power = 3428.961414 
def test_calculate_power_UFC_MMA_2():
    
    # Call the function with the test input
    result = calculate_power_UFC_MMA_2(np.pi/9, 10, 1.225, inputs)

    # Assert that the result is close to the expected value
    assert pt.approx(result, rel=1e-1) == expected_power
