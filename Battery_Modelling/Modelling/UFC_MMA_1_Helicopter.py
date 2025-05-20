import numpy as np
from Battery_Modelling.Input.Configuration_inputs import largest_real_positive_root

def calculate_power_UFC_MMA_1(incline,V,rho, inputs):
    D_parasite = 0.5*rho*inputs[3]*inputs[2]*V**2
    Tvertical = np.cos(incline)*inputs[0]
    Thorizontal = D_parasite + np.sin(incline)*inputs[0]
    T = (Tvertical**2 + Thorizontal**2)**0.5
    #Solve for vi
    alpha_T= np.cos(Tvertical/T)
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


