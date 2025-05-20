import numpy as np
from Battery_Modelling.Input.Configuration_inputs import largest_real_positive_root
numberengine_MMA2 = 4


def calculate_power_UFC_MMA_2(incline, V, rho, inputs):
    S_parasite = inputs[3]*np.sin(incline) + inputs[4]*np.cos(incline)#inputs[3]*np.sin(inputs[1]) + inputs[4]*np.cos(inputs[1])
    D_parasite = 0.5*rho*S_parasite*inputs[2]*V**2
    #Calculate thrust and power per engine
    Tvertical = np.cos(incline)*inputs[0]/numberengine_MMA2
    Thorizontal = (D_parasite + np.sin(incline)*inputs[0])/numberengine_MMA2
    T = (Tvertical**2 + Thorizontal**2)**0.5
    A_prop = inputs[6]/numberengine_MMA2
    #Solve for vi
    alpha_T= np.cos(Tvertical/T)
    A=4*(rho*A_prop)**2
    B=8*(rho*A_prop)**2*(V*np.sin(alpha_T))
    C=4*(rho*A_prop*V)**2
    D=0
    E=-T**2
    vi_roots = np.roots([A,B,C,D,E])
    vi = largest_real_positive_root(vi_roots)
    #Calculate Total Powers 
    P_induced = vi * T * numberengine_MMA2
    P_parasite = D_parasite * V #* numberengine_MMA2
    P_profile = (inputs[7]*inputs[8]*rho*inputs[9]*inputs[10]**3*inputs[5]**4*(1+3*(V/(inputs[10]*inputs[5]))**2))/8 * numberengine_MMA2
    P = (P_induced + P_parasite + P_profile) / inputs[1]
    return P

