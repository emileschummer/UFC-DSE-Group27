import sys
import os

# Add the parent directory of 'Midterm_Battery_Modelling' to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest as pt
import numpy as np
from Propeller_sizing.Model.UFC_FC_YEAH import *



