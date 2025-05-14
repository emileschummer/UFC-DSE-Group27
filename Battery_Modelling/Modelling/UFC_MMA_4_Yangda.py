import numpy as np

def calculate_power_UFC_MMA_4(incline, V, rho, inputs):
    A = np.pi*(inputs[6]**2) #m^2
    Avertical = A #individual propellor
    Ahorizontal = A #individual propellor
    L = np.cos(incline)*inputs[0]
    if V >0:
        CL = 2*L/(rho*inputs[4]*V**2)
    else:
        CL = 10000
    if CL <= inputs[5]:
        CD = inputs[2] + CL**2/inputs[3]
        Thorizontal = (0.5*rho*CD*S*V**2 + np.sin(incline)*inputs[0])/inputs[9]
        Tvertical = 0
    else:
        CL = inputs[5]
        CD = inputs[2] + CL**2/inputs[3]
        L = 0.5*rho*CL*inputs[4]*V**2 * 0.5 #parameter for wake of propellers
        Tvertical = (np.cos(incline)*inputs[0] - L)/inputs[8]
        Thorizontal = (0.5*rho*CD*inputs[4]*V**2 + np.sin(incline)*inputs[0])/inputs[9]
    Pvertical = (abs(Tvertical)**3/(2*rho*Avertical))**0.5*(inputs[8]/inputs[1])
    Phorizontal = (abs(Thorizontal)**3/(2*rho*Ahorizontal))**0.5*(inputs[9]/inputs[1])
    P = Pvertical + Phorizontal
    return P
