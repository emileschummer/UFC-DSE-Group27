import sys
import os

# Add the parent directory of 'Acceleration_try' to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import pytest as pt
import pandas as pd
from Final_UAV_Sizing.Modelling.Propeller_and_Battery_Sizing.Model.UFC_FC_YEAH import *
from Final_UAV_Sizing.Input.fixed_input_values import *
W=250 
V=10
rho=1.225  
h= 0
incline = 10
a= 5
gamma_dot = 2
aero_df = pd.read_csv(aero_csv)

# UFC 1
expected_CD_flat= 0.00012654984427
def test_flat_plate_drag_coefficient():

    result= flat_plate_drag_coefficient(V, rho, h, S_wing, L_blade, w_blade)

    assert pt.approx(result, rel=1e-6) == expected_CD_flat

#UFC 2
expected_CD_cube = 0.0168167809
def test_cube_drag_coefficient():

    result= cube_drag_coefficient(V, rho, h, S_wing, L_gimbal)

    assert pt.approx(result, rel=1e-6) == expected_CD_cube


# UFC 3
expected_CD_fus = 0.0038222928
def test_fuselage_drag_coefficient():

    Cf_fus = flat_plate_drag_coefficient(V, rho, h, S_wing, L_fus, w_fus)
    result = fuselage_drag_coefficient(L_n, L_c, Cf_fus, d_fus, S_wing)
    
    assert pt.approx(result, rel=1e-6) == expected_CD_fus

# UFC 4
CD_blade= flat_plate_drag_coefficient(V, rho, altitude, S_wing, L_blade, w_blade)
CD_poles = flat_plate_drag_coefficient(V, rho, altitude, S_wing, L_poles, w_poles)
Cf_fus = flat_plate_drag_coefficient(V, rho, altitude, S_wing, L_fus, w_fus)
CD_speaker = cube_drag_coefficient(V, rho, altitude, S_wing, L_speaker)
CD_gimbal = cube_drag_coefficient(V, rho, altitude, S_wing, L_gimbal)
CD_motor = cube_drag_coefficient(V, rho, altitude, S_wing, L_motor)
CD_fus = fuselage_drag_coefficient(L_n, L_c, Cf_fus, d_fus, S_wing)
Cf_wing = flat_plate_drag_coefficient(V, rho, altitude, S_wing, MAC, b)
Cf_hor = flat_plate_drag_coefficient(V, rho, altitude, S_wing, tail_chord, tail_span)
CD_ver = flat_plate_drag_coefficient(V, rho, altitude, S_wing, tail_chord_v, tail_chord_v)

expected_thrust_vert = 27.1734034133
expected_thrust_hor = 61.712662001
expected_CD= 0.51466598878
expected_result= expected_thrust_vert, expected_thrust_hor, expected_CD

def test_calculate_thrust_UFC_FC():

    result = calculate_thrust_UFC_FC(incline,V,rho, a, gamma_dot, W, V_vert_prop, CLmax, S_wing, aero_df, numberengines_vertical,numberengines_horizontal, propeller_wake_efficiency, CD_fus, CD_gimbal, CD_speaker, CD_motor, CD_blade, Cf_hor, CD_poles, Cf_wing, CD_ver)

    assert pt.approx(result, rel=1e-6) == expected_result

#UFC 5
vert_folder = "Final_UAV_Sizing/Input/Prop_Engine_Data/UAV_Propellers_and_Motor_Specs_Vertical.csv"
hor_folder = "Final_UAV_Sizing/Input/Prop_Engine_Data/UAV_Propellers_and_Motor_Specs_Horizontal.csv"

df_vertical = pd.read_csv(vert_folder)
df_vertical['Thrust_N'] = df_vertical[' Thrust (g) '] * 9.81 / 1000
df_horizontal = pd.read_csv(hor_folder)
df_horizontal['Thrust_N'] = df_horizontal[' Thrust (g) '] * 9.81 / 1000

expected_power_hor = 850.73956962
expected_power_vert =  889.5369868
expected_power = expected_power_hor + expected_power_vert
results = expected_power, expected_power_hor, expected_power_vert
def test_calculate_power_FC():

    result = calculate_power_FC(df_vertical,df_horizontal,incline,V,rho, a, gamma_dot, W, aero_df)

    assert pt.approx(result, rel=1e-6) == results