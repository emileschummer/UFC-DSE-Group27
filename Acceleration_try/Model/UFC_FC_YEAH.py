import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import numpy as np
import matplotlib.pyplot as plt
from Acceleration_try.Input.Config import largest_real_positive_root


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



def calculate_thrust_UFC_FC(incline,V,rho, inputs, a, gamma_dot):
    L = np.cos(incline)*inputs[0] + inputs[0]/inputs[-1] * V * gamma_dot #L is the lift force, which is the sum of the vertical component of the thrust and the lift force of the propellers
    if V >0:
        CL = 2*L/(rho*inputs[4]*V**2)
    else:
        CL = 10000#to jump into else statement
    if CL <= inputs[5]:
        CD = inputs[2] + CL**2/inputs[3]
        D_parasite = 0.5*rho*CD*inputs[4]*V**2 #D_parasite includes both the parasite drag of the fusealge and the drag of the lifting force of the wing
        Thorizontal = (D_parasite + np.sin(incline)*inputs[0]) + inputs[0]/inputs[-1] * a
        Tvertical = 0
        
    else:
        #Vertical propellers kick in to aid with lift
        CL = inputs[5]#np.sqrt(inputs[3]*inputs[2]) 
        CD = inputs[2] + CL**2/inputs[3]
        L = 0.5*rho*CL*inputs[4]*V**2 * inputs[7]  #parameter for wake of propellers
        D_parasite = 0.5*rho*CD*inputs[4]*V**2#D_parasite includes both the parasite drag of the fusealge and the drag of the lifting force of the wing
        #Calculate thrust and power per engine
        Tvertical = (np.cos(incline)*inputs[0] - L)/inputs[16]
        Thorizontal = (D_parasite + np.sin(incline)*inputs[0]) + inputs[0]/inputs[-1] * a
        
    return Tvertical, Thorizontal
    