import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import numpy as np
import matplotlib.pyplot as plt
from Final_UAV_Sizing.Input.fixed_input_values import g
import Input.RaceData.Strava_input_csv as sva

def flat_plate_drag_coefficient(V, rho, h, S_wing, L, w):
    if V <= 0:
        Cf_i = 0
    else:
        T0 = 288.15
        T = T0 + -0.0065 * h
        Re= rho * V * L / 1.81e-5  # Reynolds number, assuming a kinematic viscosity of air at sea level
        a= np.sqrt(1.4 * 287.05 * T)
        Cf_i= 0.455/ ((np.log10(Re))**2.58 * (1 + 0.144 * (V/a)**2)**0.65) * L*w/S_wing
    return Cf_i

def cube_drag_coefficient(V, rho, h, S_wing, L):
    if V <= 0:
        CD_cube = 0
        return CD_cube
    else:
        T0 = 288.15
        T = T0 + -0.0065 * h
        Re= rho * V * L / 1.81e-5  # Reynolds number, assuming a kinematic viscosity of air at sea level
        a= np.sqrt(1.4 * 287.05 * T)
        CD_cube= (1.1 + 20/np.sqrt(Re)) * (1 + 0.15 * (V/a)**2) * L**2/S_wing
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


def calculate_thrust_UFC_FC(incline,V,rho, a, gamma_dot, W, V_vert_prop, CLmax, S_wing,aero_df, numberengines_vertical,numberengines_horizontal, propeller_wake_efficiency, CD_fus, CD_gimbal, CD_speaker, CD_motor, Cf_blade, Cf_stab, Cf_poles):
    L_req = np.cos(incline)*W + W/g * V * gamma_dot #vertical force required for flight (stationary or not)
    if V > V_vert_prop:
        CL = 2*L_req/(rho*S_wing*V**2)
        CD_wing = np.interp(CL, aero_df["CL_corrected"], aero_df["CD_vlm"])
        CD= CD_fus + CD_gimbal + CD_speaker + CD_wing + 4 * CD_motor + 2 * Cf_poles+ 4 * Cf_blade + 3 * Cf_stab #Total drag coefficient
        D_wing = 0.5*rho*CD*S_wing*V**2
        T_horizontal = ((D_wing + np.sin(incline)*W) + W/g * a)/ numberengines_horizontal #Thrust per horizontal propeller
        T_vertical = 0
        
    else:
        CL = CLmax
        CD_wing = np.interp(CL, aero_df["CL_corrected"], aero_df["CD_vlm"])
        CD= CD_fus + CD_gimbal + CD_speaker + CD_wing + 4 * Cf_blade + 3 * Cf_stab #Total drag coefficient
        D_wing = 0.5*rho*CD*S_wing*V**2
        T_horizontal = ((D_wing + np.sin(incline)*W) + W/g * a)/ numberengines_horizontal #Thrust per horizontal propeller
        L_wing = 0.5*rho*CL*S_wing*V**2 * propeller_wake_efficiency  #Lifting force of the wing, parameter for wake of propellers
        L_prop = L_req - L_wing
        T_vertical = L_prop/numberengines_vertical #Thrust per vertical propeller

    if T_horizontal < 0:
        T_horizontal = 0       
    return T_vertical,T_horizontal, CD

def calculate_power_FC(df_vertical,df_horizontal,incline,V,rho, a, gamma_dot, W, V_vert_prop, CLmax, S_wing, aero_df, numberengines_vertical,numberengines_horizontal, propeller_wake_efficiency,L_fus,L_n,L_c, d_fus, w_fus, L_blade, w_blade, L_stab, w_stab, L_poles, w_poles, L_motor, L_gimbal, L_speaker):
    altitude = sva.altitude_from_density(rho)
    Cf_blade= flat_plate_drag_coefficient(V, rho, altitude, S_wing, L_blade, w_blade)
    Cf_stab = flat_plate_drag_coefficient(V, rho, altitude,S_wing,L_stab, w_stab)
    Cf_poles = flat_plate_drag_coefficient(V, rho, altitude, S_wing, L_poles, w_poles)
    Cf_fus = flat_plate_drag_coefficient(V, rho, altitude, S_wing, L_fus, w_fus)
    CD_speaker = cube_drag_coefficient(V, rho, altitude, S_wing, L_speaker)
    CD_gimbal = cube_drag_coefficient(V, rho, altitude, S_wing, L_gimbal)
    CD_motor = cube_drag_coefficient(V, rho, altitude, S_wing, L_motor)
    CD_fus = fuselage_drag_coefficient(L_n, L_c, Cf_fus, d_fus, S_wing)

    T_vertical, T_horizontal, CD = calculate_thrust_UFC_FC(incline,V,rho, a, gamma_dot, W, V_vert_prop, CLmax, S_wing,aero_df, numberengines_vertical,numberengines_horizontal, propeller_wake_efficiency, CD_fus, CD_gimbal, CD_speaker, CD_motor, Cf_blade, Cf_stab, Cf_poles)
    
    #Vertical power
    max_thrust = df_vertical['Thrust_N'].max()
    if T_vertical > max_thrust:
        print(f"{T_vertical-max_thrust} Vertical thrust exceeded")
        T_vertical = max_thrust
        #raise ValueError(f"T_vertical ({T_vertical:.2f} N) exceeds the maximum thrust in the CSV ({max_thrust:.2f} N).")
    
    else: P_vertical = np.interp(T_vertical, df_vertical['Thrust_N'], df_vertical[' Power (W) '])*numberengines_vertical
    
    # Horizontal power
    max_thrust = df_horizontal['Thrust_N'].max()
    if T_horizontal > max_thrust:
        #print(f"{T_horizontal-max_thrust} Horizontal thrust exceeded")
        T_horizontal = max_thrust
        #raise ValueError(f"T_horizontal ({T_horizontal:.2f} N) exceeds the maximum thrust in the CSV ({max_thrust:.2f} N).")
    
    else:
        P_horizontal = np.interp(T_horizontal, df_horizontal['Thrust_N'], df_horizontal[' Power (W) ']) * numberengines_horizontal
    P = P_vertical + P_horizontal
    return P