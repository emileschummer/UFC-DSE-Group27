import numpy as np
from Midterm_Battery_Modelling.Input.Configuration_inputs import largest_real_positive_root

def calculate_power_UFC_MMA_1(incline,V,rho, inputs):
    D_parasite = 0.5*rho*inputs[3]*inputs[2]*V**2
    Tvertical = np.cos(incline)*inputs[0]
    Thorizontal = D_parasite + np.sin(incline)*inputs[0]
    T = (Tvertical**2 + Thorizontal**2)**0.5
    #Solve for vi
    alpha_T= np.arccos(Tvertical/T)
    A=4*(rho*inputs[5])**2
    B=8*(rho*inputs[5])**2*(V*np.sin(alpha_T))
    C=4*(rho*inputs[5]*V)**2
    D=0
    E=-T**2
    vi_roots = np.roots([A,B,C,D,E])
    vi = largest_real_positive_root(vi_roots)
    #Calculate Powers
    P_induced = vi * T
    P_parasite = D_parasite * V
    P_profile = (inputs[6]*inputs[7]*rho*inputs[8]*inputs[9]**3*inputs[4]**4*(1+3*(V/(inputs[9]*inputs[4]))**2))/8
    P = (P_induced + P_parasite + P_profile) / inputs[1]
    return P
"""
import matplotlib.pyplot as plt

velocities = np.linspace(0, 100, 100)
incline = 0
rho = 1.225
inputs = [W,eta,CD0_MMA1,S_parasite_MMA1,r_MMA1,A_prop_MMA1,N_blades_MMA1,chord_blade_MMA1,cd_blade_MMA1,omega_MMA1,solidity_MMA1]

P_list = []
P_induced_list = []
P_parasite_list = []
P_profile_list = []

for V in velocities:
    try:
        P, P_induced, P_parasite, P_profile = calculate_power_UFC_MMA_1(incline, V, rho, inputs)
    except Exception:
        P, P_induced, P_parasite, P_profile = np.nan, np.nan, np.nan, np.nan
    P_list.append(P)
    P_induced_list.append(P_induced)
    P_parasite_list.append(P_parasite)
    P_profile_list.append(P_profile)

plt.plot(velocities, P_induced_list, label='P_induced')
plt.plot(velocities, P_parasite_list, label='P_parasite')
plt.plot(velocities, P_profile_list, label='P_profile')
plt.plot(velocities, P_list, label='P (Total)')
plt.xlabel('Velocity (m/s)')
plt.ylabel('Power (W)')
plt.title('Power vs Velocity')
plt.legend()
plt.grid(True)
plt.show()"""


