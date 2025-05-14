import numpy as np

def calculate_power_UFC_MMA_1(incline,V,rho, inputs):
    D = 0.5*rho*inputs[3]*inputs[2]*V**2
    Tvertical = np.cos(incline)*inputs[0]
    Thorizontal = D + np.sin(incline)*inputs[0]
    T = (Tvertical**2 + Thorizontal**2)**0.5
    P = (abs(T)**3/(2*rho*inputs[4]))**0.5/inputs[1]
    return P