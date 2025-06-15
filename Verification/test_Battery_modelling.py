import sys
import os

# Add the parent directory of 'Acceleration_try' to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest as pt
import pandas as pd
from Final_UAV_Sizing.Modelling.Propeller_and_Battery_Sizing.Model.UFC_FC_YEAH import *
from Final_UAV_Sizing.Input.fixed_input_values import *
from Final_UAV_Sizing.Modelling.Propeller_and_Battery_Sizing.Model.Battery_modelling import *

import numpy as np
import pandas as pd
from unittest.mock import patch
W = 250
aero_df = pd.read_csv(aero_csv)
vert_folder = "Final_UAV_Sizing/Input/Prop_Engine_Data/UAV_Propellers_and_Motor_Specs_Vertical.csv"
hor_folder = "Final_UAV_Sizing/Input/Prop_Engine_Data/UAV_Propellers_and_Motor_Specs_Horizontal.csv"
df_vertical = pd.read_csv(vert_folder)
df_vertical['Thrust_N'] = df_vertical[' Thrust (g) '] * 9.81 / 1000
df_horizontal = pd.read_csv(hor_folder)
df_horizontal['Thrust_N'] = df_horizontal[' Thrust (g) '] * 9.81 / 1000

calculate_power = calculate_power_FC
race_data = pd.DataFrame({
        " distance": [0, 10],
        " time": [0, 1],
        " velocity_smooth": [0, 10],
        " grade_smooth": [0, 5],
        " altitude": [0, 10]
    })

def test_simulate_1_battery():

    outcome= simulate_1_battery(df_vertical,df_horizontal,race_data, calculate_power, W, V_vert_prop, CLmax, S_wing, aero_df, numberengines_vertical,numberengines_horizontal, propeller_wake_efficiency,PL_power,L_fus,L_n,L_c,L_blade,L_stab, d_fus, w_fus, w_blade, w_stab, L_poles, w_poles, L_motor, L_gimbal, L_speaker)

    assert len(outcome[1]) == 2
    assert outcome[2][0] == PL_power + (calculate_power_FC(df_vertical,df_horizontal,0,0,0, 0, 0, W, V_vert_prop, CLmax, S_wing, aero_df, numberengines_vertical,numberengines_horizontal, propeller_wake_efficiency,L_fus,L_n,L_c, d_fus, w_fus, L_blade, w_blade, L_stab, w_stab, L_poles, w_poles, L_motor, L_gimbal, L_speaker))

