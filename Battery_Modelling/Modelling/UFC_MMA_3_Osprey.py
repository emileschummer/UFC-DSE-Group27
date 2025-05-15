import numpy as np
numberengines_MMA3=2
def calculate_power_UFC_MMA_3(incline, V, rho, inputs):
    A = np.pi*(inputs[6]**2) #m^2
    L = np.cos(incline)*inputs[0]
    if V >0:
        CL = 2*L/(rho*inputs[4]*V**2)
    else:
        CL = 10000#to jump into else statement
    if CL <= inputs[5]:
        CD = inputs[2] + CL**2/inputs[3]
        T = (0.5*rho*CD*inputs[4]*V**2 + np.sin(incline)*inputs[0])/numberengines_MMA3
    else:
        CL = inputs[5]
        CD = inputs[2] + CL**2/inputs[3]
        L = 0.5*rho*CL*inputs[4]*V**2 *inputs[7]
        Tvertical = np.cos(incline)*inputs[0] - L
        Thorizontal = 0.5*rho*CD*inputs[4]*V**2 + np.sin(incline)*inputs[0]
        T = (Tvertical**2 + Thorizontal**2)**0.5/numberengines_MMA3
    P = (abs(T)**3/(2*rho*A))**0.5*(numberengines_MMA3/inputs[1])
    return P

