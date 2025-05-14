import numpy as np
numberengines_vertical_MMA4 = 4
numberengines_horizontal_MMA4 = 1


def calculate_power_UFC_MMA_4(incline,V,rho, inputs):
    A = np.pi*(inputs[6]**2) #m^2
    Avertical = A 
    Ahorizontal = A
    L = np.cos(incline)*inputs[0]
    if V >0:
        CL = 2*L/(rho*inputs[4]*V**2)
    else:
        CL = 10000
    if CL <= inputs[5]:
        CD = inputs[2] + CL**2/inputs[3]
        Thorizontal = (0.5*rho*CD*inputs[4]*V**2 + np.sin(incline)*inputs[0])/numberengines_horizontal_MMA4
        Tvertical = 0
    else:
        CL = inputs[5]
        CD = inputs[2] + CL**2/inputs[3]
        L = 0.5*rho*CL*inputs[4]*V**2 * 0.5 #parameter for wake of propellers
        Tvertical = (np.cos(incline)*inputs[0] - L)/numberengines_vertical_MMA4
        Thorizontal = (0.5*rho*CD*inputs[4]*V**2 + np.sin(incline)*inputs[0])/numberengines_horizontal_MMA4
    Pvertical = (abs(Tvertical)**3/(2*rho*Avertical))**0.5*(numberengines_vertical_MMA4/inputs[1])
    Phorizontal = (abs(Thorizontal)**3/(2*rho*Ahorizontal))**0.5*(numberengines_horizontal_MMA4/inputs[1])
    P = Pvertical + Phorizontal
    return P
