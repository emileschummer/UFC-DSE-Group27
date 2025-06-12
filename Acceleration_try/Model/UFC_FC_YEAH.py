import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import numpy as np
import matplotlib.pyplot as plt
from Acceleration_try.Input.Config import largest_real_positive_root
from Acceleration_try.Input import Strava_input_csv as sva


import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

def flat_plate_drag_coefficient(V, rho, h, L):
    T0 = 288.15
    T = T0 + -0.0065 * h
    Re= rho * V * L / 1.81e-5  # Reynolds number, assuming a kinematic viscosity of air at sea level
    a= np.sqrt(1.4 * 287.05 * T)
    Cf_i= 0.455/ ((np.log10(Re))**2.58 * (1 + 0.144 * (V/a)**2)**0.65)
    return Cf_i

def cube_drag_coefficient(V, rho, h, S_wing):
    T0 = 288.15
    T = T0 + -0.0065 * h
    L_cube = 0.12
    Re= rho * V * L_cube / 1.81e-5  # Reynolds number, assuming a kinematic viscosity of air at sea level
    a= np.sqrt(1.4 * 287.05 * T)
    CD_cube= (1.1 + 20/np.sqrt(Re)) * (1 + 0.15 * (V/a)**2) * L_cube**2/S_wing
    return CD_cube

def fuselage_drag_coefficient(L_n, L_c, Cf_fus, d, S_wing):
    S_nose_tail = np.pi * d/2 * np.sqrt(L_n**2 + (d/2)**2) +2 * np.pi * (d/2)**2 
    S_cabin= np.pi * d * L_c 
    S_wet_fus= 2 * S_nose_tail + S_cabin
    L = 2 * L_n + L_c
    IF_fus= 1.05
    FF_fus= 1 + 60/ (L/d)**3 + 0.0025 * (L/d)**2 
    CD_fus= Cf_fus * IF_fus * FF_fus * S_wet_fus / S_wing
    return CD_fus


def calculate_thrust_UFC_FC(incline,V,rho, a, gamma_dot, W, V_vert_prop, CLmax, S_wing,aero_df, numberengines_vertical,numberengines_horizontal, propeller_wake_efficiency, CD_fus, CD_cube, Cf_blade, Cf_stab):
    L_req = np.cos(incline)*W + W/g * V * gamma_dot #vertical force required for flight (stationary or not)
    if V > V_vert_prop:
        CL = 2*L_req/(rho*S_wing*V**2)
        CD_wing = np.interp(CL, aero_df["CL_corrected"], aero_df["CD_vlm"])
        CD= CD_fus + CD_cube + CD_wing + 4 * Cf_blade + 3 * Cf_stab #Total drag coefficient
        D_wing = 0.5*rho*CD*S_wing*V**2
        T_horizontal = ((D_wing + np.sin(incline)*W) + W/g * a)/ numberengines_horizontal #Thrust per horizontal propeller
        T_vertical = 0
        
    else:
        CL = CLmax
        CD_wing = np.interp(CL, aero_df["CL_corrected"], aero_df["CD_vlm"])
        CD= CD_fus + CD_cube + CD_wing + 4 * Cf_blade + 3 * Cf_stab #Total drag coefficient
        D_wing = 0.5*rho*CD*S_wing*V**2
        T_horizontal = ((D_wing + np.sin(incline)*W) + W/g * a)/ numberengines_horizontal #Thrust per horizontal propeller
        L_wing = 0.5*rho*CL*S_wing*V**2 * propeller_wake_efficiency  #Lifting force of the wing, parameter for wake of propellers
        L_prop = L_req - L_wing
        T_vertical = L_prop/numberengines_vertical #Thrust per vertical propeller
           
    return T_vertical,T_horizontal

def calculate_power_FC(df_vertical,df_horizontal,incline,V,rho, a, gamma_dot, W, V_vert_prop, CLmax, S_wing, aero_df, numberengines_vertical,numberengines_horizontal, propeller_wake_efficiency,L_fus,L_n,L_c,d,L_blade,L_stab):
    Cf_fus = flat_plate_drag_coefficient(V, rho, sva.altitude_from_density(rho), L_fus)
    CD_fus = fuselage_drag_coefficient(L_n, L_c, Cf_fus, d, S_wing)
    CD_cube = cube_drag_coefficient(V, rho, sva.altitude_from_density(rho), S_wing)
    Cf_blade = flat_plate_drag_coefficient(V, rho, sva.altitude_from_density(rho), L_blade)
    Cf_stab = flat_plate_drag_coefficient(V, rho, sva.altitude_from_density(rho), L_stab)

    T_vertical, T_horizontal = calculate_thrust_UFC_FC(incline,V,rho, a, gamma_dot, W, V_vert_prop, CLmax, S_wing,aero_df, numberengines_vertical,numberengines_horizontal, propeller_wake_efficiency, CD_fus, CD_cube, Cf_blade, Cf_stab)
    
    #Vertical power
    max_thrust = df_vertical['Thrust_N'].max()
    if T_vertical > max_thrust:
        print(f"{T_vertical-max_thrust} Vertical thrust exceeded")
        T_vertical = max_thrust
        #raise ValueError(f"T_vertical ({T_vertical:.2f} N) exceeds the maximum thrust in the CSV ({max_thrust:.2f} N).")
    P_vertical = np.interp(T_vertical, df_vertical['Thrust_N'], df_vertical[' Power (W) '])*numberengines_vertical
    
    # Horizontal power
    max_thrust = df_horizontal['Thrust_N'].max()
    if T_horizontal > max_thrust:
        #print(f"{T_horizontal-max_thrust} Horizontal thrust exceeded")
        T_horizontal = max_thrust
        #raise ValueError(f"T_horizontal ({T_horizontal:.2f} N) exceeds the maximum thrust in the CSV ({max_thrust:.2f} N).")
    P_horizontal = np.interp(T_horizontal, df_horizontal['Thrust_N'], df_horizontal[' Power (W) ']) * numberengines_horizontal
    P = P_vertical + P_horizontal
    return P
