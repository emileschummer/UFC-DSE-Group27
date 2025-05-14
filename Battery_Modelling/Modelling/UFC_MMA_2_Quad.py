import numpy as np
numberengine_MMA2 = 4


def calculate_power_UFC_MMA_2(incline, V, rho, inputs):
    S = inputs[3]*np.sin(inputs[1]) + inputs[4]*np.cos(inputs[1])
    A = inputs[5]/numberengine_MMA2
    D = 0.5*rho*S*inputs[2]*V**2
    Tvertical = np.cos(incline)*inputs[0]
    Thorizontal = (D + np.sin(incline)*inputs[0])
    T = (Tvertical**2 + Thorizontal**2)**0.5/numberengine_MMA2
    P = (abs(T)**3/(2*rho*A))**0.5*(numberengine_MMA2/inputs[1])
    return P
