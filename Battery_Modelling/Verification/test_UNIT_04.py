import sys
import os

# Add the parent directory of 'Battery_Modelling' to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import pytest as pt
import numpy as np
from Battery_Modelling.Modelling.UFC_MMA_2_Quad import calculate_power_UFC_MMA_2

# Test parameters
CD = 0.105 #https://dspace-erf.nlr.nl/server/api/core/bitstreams/0a756857-3708-4250-9524-bdbcc0020d33/content

W = 250 #N

A = 0.3
eta = 0.8
totalA = (1.041/2)**2*np.pi
numberengines = 4
A = totalA/numberengines
S = 0.16
expected_power = 3428.961414 
def test_calculate_power_UFC_MMA_2():
    
    # Call the function with the test input
    result = calculate_power_UFC_MMA_2(np.pi/9, 10, 1.225)

    # Assert that the result is close to the expected value
    assert pt.approx(result, rel=1e-1) == expected_power
