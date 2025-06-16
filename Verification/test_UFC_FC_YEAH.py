import sys
import os

# Add the parent directory of 'Acceleration_try' to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

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

# UNIT 03
expected_CD= 0.000141103
def test_flat_plate_drag_coefficient():

    result= flat_plate_drag_coefficient(V, rho, h, S_wing, L_blade, w_blade)

    assert pt.approx(result, rel=1e-6) == expected_CD

#UNIT 04
expected_CD_cube = 0.008426384
def test_cube_drag_coefficient():

    result= cube_drag_coefficient(V, rho, h, S_wing, L_gimbal)

    assert pt.approx(result, rel=1e-6) == expected_CD_cube


# UNIT 05
expected_CD_fus = 0.004261856
def test_fuselage_drag_coefficient():

    Cf_fus = flat_plate_drag_coefficient(V, rho, h, S_wing, L_fus, w_fus)
    result = fuselage_drag_coefficient(L_n, L_c, Cf_fus, d_fus, S_wing)
    
    assert pt.approx(result, rel=1e-6) == expected_CD_fus

# SUBSYSTEM 01
CF_fus = flat_plate_drag_coefficient(V, rho, h, S_wing, L_fus, w_fus)
CD_fus = fuselage_drag_coefficient(L_n, L_c, CF_fus, d_fus, S_wing)
CD_gimbal = cube_drag_coefficient(V, rho, h, S_wing, L_gimbal)
CD_speaker = cube_drag_coefficient(V, rho, h, S_wing, L_speaker)
CD_motor = flat_plate_drag_coefficient(V, rho, h, S_wing, L_motor, w_blade)
Cf_blade = flat_plate_drag_coefficient(V, rho, h, S_wing, L_blade, w_blade)
Cf_stab = flat_plate_drag_coefficient(V, rho, h, S_wing, L_stab, w_stab)
Cf_poles = flat_plate_drag_coefficient(V, rho, h, S_wing, L_poles, w_poles)

expected_thrust_vert = 32.10402841
expected_thrust_hor = 33.59434087
expected_CD= 0.34431526
expected_result= expected_thrust_vert, expected_thrust_hor, expected_CD

def test_calculate_thrust_UFC_FC():

    result = calculate_thrust_UFC_FC(incline,V,rho, a, gamma_dot, W, V_vert_prop, CLmax, S_wing,aero_df, numberengines_vertical,numberengines_horizontal, propeller_wake_efficiency, CD_fus, CD_gimbal, CD_speaker, CD_motor, Cf_blade, Cf_stab, Cf_poles)

    assert pt.approx(result, rel=1e-6) == expected_result

#SUBSYSTEM 02
vert_folder = "Final_UAV_Sizing/Input/Prop_Engine_Data/UAV_Propellers_and_Motor_Specs_Vertical.csv"
hor_folder = "Final_UAV_Sizing/Input/Prop_Engine_Data/UAV_Propellers_and_Motor_Specs_Horizontal.csv"

df_vertical = pd.read_csv(vert_folder)
df_vertical['Thrust_N'] = df_vertical[' Thrust (g) '] * 9.81 / 1000
df_horizontal = pd.read_csv(hor_folder)
df_horizontal['Thrust_N'] = df_horizontal[' Thrust (g) '] * 9.81 / 1000

expected_power =  1535.55819120
def test_calculate_power_FC():

    result = calculate_power_FC(df_vertical, df_horizontal, incline, V, rho, a, gamma_dot, W, V_vert_prop, CLmax, S_wing, aero_df, numberengines_vertical, numberengines_horizontal, propeller_wake_efficiency,L_fus,L_n,L_c, d_fus, w_fus, L_blade, w_blade, L_stab, w_stab, L_poles, w_poles, L_motor, L_gimbal, L_speaker)

    assert pt.approx(result, rel=1e-6) == expected_power

print(calculate_power_FC(df_vertical, df_horizontal, incline, V, rho, a, gamma_dot, W, V_vert_prop, CLmax, S_wing, aero_df, numberengines_vertical, numberengines_horizontal, propeller_wake_efficiency,L_fus,L_n,L_c, d_fus, w_fus, L_blade, w_blade, L_stab, w_stab, L_poles, w_poles, L_motor, L_gimbal, L_speaker))