import sys
import os

# Add the parent directory of 'Battery_Modelling' to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import pytest as pt
import numpy as np
from Battery_Modelling.Modelling.UFC_MMA_1_Helicopter import calculate_power_UFC_MMA_1

# Test parameters
CD =0.105 #https://dspace-erf.nlr.nl/server/api/core/bitstreams/0a756857-3708-4250-9524-bdbcc0020d33/content 
S = 0.16 # http://eprints.gla.ac.uk/116394/1/116394.pdf
W = 250 #N

diameter = 1.041 #https://dspace-erf.nlr.nl/server/api/core/bitstreams/9dc27553-90f0-4209-b744-0adee5c75f27/content 
A = (diameter/2)**2*np.pi
eta = 0.8

expected_power= 3428.961415 # Expected value for power (to be calculated based on the formula)

def test_calculate_power_UFC_MMA_1():
   
    
    # Call the function with the test input
    result = calculate_power_UFC_MMA_1(np.pi/9, 10, 1.225)

    # Assert that the result is close to the expected value
    assert pt.approx(result, rel=1e-1) == expected_power

