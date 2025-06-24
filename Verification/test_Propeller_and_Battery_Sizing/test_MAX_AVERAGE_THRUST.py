import sys
import os

# Add the parent directory of 'Acceleration_try' to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import pytest as pt
import pandas as pd
from Final_UAV_Sizing.Modelling.Propeller_and_Battery_Sizing.Model.UFC_FC_YEAH import *
from Final_UAV_Sizing.Input.fixed_input_values import *
from Final_UAV_Sizing.Modelling.Propeller_and_Battery_Sizing.Model.MAX_AVERAGE_THUST import analyze_race_thrust
import Final_UAV_Sizing.Input.RaceData.Strava_input_csv as sva

