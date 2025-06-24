import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from scipy.interpolate import interp1d

from Propeller_sizing.Model.UFC_FC_YEAH import *
from Propeller_sizing.Input.Strava_input_csv import air_density_isa
from Final_UAV_Sizing.Input.fixed_input_values import *
W= 25*9.81
aero_df = pd.read_csv('Propeller_sizing/Model/aero.csv')

# Load race and propeller data
df_vertical = pd.read_csv('Propeller_sizing/Input/Prop_Engine_Data/UAV_Propellers_and_Motor_Specs_Vertical.csv')
df_vertical['Thrust_N'] = df_vertical[' Thrust_g '] * g / 1000
df_horizontal = pd.read_csv('Propeller_sizing/Input/Prop_Engine_Data/UAV_Propellers_and_Motor_Specs_Horizontal.csv')
df_horizontal['Thrust_N'] = df_horizontal[' Thrust_g '] * g / 1000

incline = -10*np.pi/180
V= 120/3.6
a= 0
gamma_dot = 0
rho = air_density_isa(1000)
altitude = sva.altitude_from_density(rho)
CD_blade= flat_plate_drag_coefficient(V, rho, altitude, S_wing, L_blade, w_blade)
Cf_stab = flat_plate_drag_coefficient(V, rho, altitude,S_wing,L_stab, w_stab)
CD_poles = flat_plate_drag_coefficient(V, rho, altitude, S_wing, L_poles, w_poles)
Cf_fus = flat_plate_drag_coefficient(V, rho, altitude, S_wing, L_fus, w_fus)
CD_speaker = cube_drag_coefficient(V, rho, altitude, S_wing, L_speaker)
CD_gimbal = cube_drag_coefficient(V, rho, altitude, S_wing, L_gimbal)
CD_motor = cube_drag_coefficient(V, rho, altitude, S_wing, L_motor)
CD_fus = fuselage_drag_coefficient(L_n, L_c, Cf_fus, d_fus, S_wing)
Cf_wing = flat_plate_drag_coefficient(V, rho, altitude, S_wing, MAC, b)
Cf_hor = flat_plate_drag_coefficient(V, rho, altitude, S_wing, tail_chord, tail_span)
CD_ver = flat_plate_drag_coefficient(V, rho, altitude, S_wing, tail_chord_v, tail_chord_v)

print(calculate_thrust_UFC_FC(incline,V,rho, a, gamma_dot, W, V_vert_prop, CLmax, S_wing,aero_df, numberengines_vertical,numberengines_horizontal, propeller_wake_efficiency, CD_fus, CD_gimbal, CD_speaker, CD_motor, CD_blade, Cf_hor, CD_poles, Cf_wing, CD_ver))