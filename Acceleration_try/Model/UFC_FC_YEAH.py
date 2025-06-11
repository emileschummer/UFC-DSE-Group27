import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import numpy as np
import matplotlib.pyplot as plt
from Acceleration_try.Input.Config import largest_real_positive_root


g = 9.81
def get_RPM_efficiency_vertical(Tvertical):
    # Load or define your data arrays
    thrust_data = np.array([1733, 1856, 2007, 2172, 2295, 2371, 2619, 2804, 2960, 3199, 3422, 3584, 3742, 3963, 4082, 4272, 4688, 5177, 6145, 7200])

    rpm_data = np.array([1284, 1342, 1404, 1468, 1513, 1591, 1656, 1713, 1768, 1828, 1911, 1966, 2003, 2061, 2112, 2160, 2303, 2411, 2651, 2917])

    efficiency_data = np.array([14.41, 14.1, 13.88, 13.57, 13.12, 12.37, 12.56, 12.44, 12.14, 12.08, 11.46, 11.3, 11.08, 11.0, 10.74, 10.55, 10.1, 9.78, 9.04, 8.32])

    # Interpolate to get RPM and efficiency for given thrust
    rpm = np.interp(Tvertical, thrust_data, rpm_data)
    efficiency = np.interp(Tvertical, thrust_data, efficiency_data)

    return rpm, efficiency

def get_RPM_efficiency_horizontal(Thorizontal):
    # Load or define your data arrays
    thrust_data = 0

    rpm_data = 0

    efficiency_data = 0

    # Interpolate to get RPM and efficiency for given thrust
    rpm = np.interp(Thorizontal , thrust_data , rpm_data)
    efficiency = np.interp(Thorizontal , thrust_data , efficiency_data)

    return rpm , efficiency

def flat_plate_drag_coefficient(V, rho, L, T):
    Re= rho * V * L / 1.81e-5  # Reynolds number, assuming a kinematic viscosity of air at sea level
    a= np.sqrt(1.4 * 287.05 * T)
    CD_fp= 0.455/ ((np.log10(Re))**2.58 * (1 + 0.144 * (V/a)**2)**0.65)
    return CD_fp

def sphere_drag_coefficient(V, rho, L):
    Re= rho * V * L / 1.81e-5
    term1 = 24.0 / Re
    term2 = 2.6 * (Re / 5.0) / (1.0 + (Re / 5.0)**1.52)
    term3 = 0.411 * (Re / 2.63e5)**(-7.94) / (1.0 + (Re / 2.63e5)**(-8.00))
    term4 = 0.25 * (Re / 1e6) / (1.0 + (Re / 1e6))

    CD_sphere = term1 + term2 + term3 + term4
    return CD_sphere

def fuselage_drag_coefficient(K_n, K_c, d, V, rho, L, T):
    CD_fp = flat_plate_drag_coefficient(V, rho, L, T)
    R= d/2
    e= np.sqrt(1 - (R/L)**2)
    S_wet_cabin = np.pi * d * L  # Wet surface area of the cabin
    S_wet_nose = np.pi * R**2 * (1 + (L/(R*e)) * np.arcsin(e))
    S_front = (d/2)**2 *np.pi
    S_wet = S_wet_cabin + S_wet_nose

    CD_fus= (K_n * S_wet_nose/S_wet + K_c * S_wet_cabin/S_wet) * CD_fp *S_wet/S_front
    return CD_fus


def calculate_thrust_UFC_FC(incline,V,rho, a, gamma_dot, W, V_vert_prop, CLmax, S_wing, CD0_wing, piAe, numberengines_vertical,numberengines_horizontal, propeller_wake_efficiency):
    L_req = np.cos(incline)*W + W/g * V * gamma_dot #vertical force required for flight (stationary or not)
    if V > V_vert_prop:
        CL = 2*L_req/(rho*S_wing*V**2)
        CD = CD0_wing + CL**2/piAe
        D_wing = 0.5*rho*CD*S_wing*V**2
        T_horizontal = ((D_wing + np.sin(incline)*W) + W/g * a)/ numberengines_horizontal #Thrust per horizontal propeller
        T_vertical = 0
        
    else:
        CL = CLmax
        CD = CD0_wing + CL**2/piAe
        D_wing = 0.5*rho*CD*S_wing*V**2
        T_horizontal = ((D_wing + np.sin(incline)*W) + W/g * a)/ numberengines_horizontal #Thrust per horizontal propeller
        L_wing = 0.5*rho*CL*S_wing*V**2 * propeller_wake_efficiency  #Lifting force of the wing, parameter for wake of propellers
        L_prop = L_req - L_wing
        T_vertical = L_prop/numberengines_vertical #Thrust per vertical propeller
           
    return T_vertical, T_horizontal

def calculate_power_FC(df_vertical,df_horizontal,incline,V,rho, a, gamma_dot, W, V_vert_prop, CLmax, S_wing, CD0_wing, piAe, numberengines_vertical,numberengines_horizontal, propeller_wake_efficiency):
    T_vertical, T_horizontal = calculate_thrust_UFC_FC(incline,V,rho, a, gamma_dot, W, V_vert_prop, CLmax, S_wing, CD0_wing, piAe, numberengines_vertical,numberengines_horizontal, propeller_wake_efficiency)
    
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
