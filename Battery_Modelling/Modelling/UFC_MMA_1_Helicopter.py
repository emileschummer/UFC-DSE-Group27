import numpy as np

def calculate_power_UFC_MMA_1(incline,V,rho, inputs):
    D = 0.5*rho*S*CD*V**2
    Tvertical = np.cos(incline)*W
    Thorizontal = D + np.sin(incline)*W
    T = (Tvertical**2 + Thorizontal**2)**0.5
    P = (abs(T)**3/(2*rho*inputs[5]))**0.5/inputs[1]
    return P