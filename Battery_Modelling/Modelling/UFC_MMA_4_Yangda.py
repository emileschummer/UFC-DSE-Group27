import numpy as np
numberengines_vertical_MMA4 = 4
numberengines_horizontal_MMA4 = 1


def calculate_power_UFC_MMA_4(incline,V,rho, inputs, max_iter=1000, tol=1e-3):
    A = np.pi*(inputs[6]**2) #m^2
    L = np.cos(incline)*inputs[0]
    if V >0:
        CL = 2*L/(rho*inputs[4]*V**2)
    else:
        CL = 10000#to jump into else statement
    if CL <= inputs[5]:
        CD = inputs[2] + CL**2/inputs[3]
        D = 0.5*rho*CD*inputs[4]*V**2
        T = (D + np.sin(incline)*inputs[0])/numberengines_horizontal_MMA4
        P = T*V*(numberengines_horizontal_MMA4/inputs[1])
    else:
        CL = inputs[5]
        CD = inputs[2] + CL**2/inputs[3]
        L = 0.5*rho*CL*inputs[4]*V**2 * inputs[7]  #parameter for wake of propellers
        D = 0.5*rho*CD*inputs[4]*V**2
        Tvertical = (np.cos(incline)*inputs[0] - L)/numberengines_vertical_MMA4
        Thorizontal = (D + np.sin(incline)*inputs[0])/numberengines_horizontal_MMA4
        alpha_T= 0
        T_hover= inputs[0]/numberengines_vertical_MMA4
        V_ind_hover= (T_hover/(2*rho*A))**0.5
        vi = V_ind_hover  # initial guess
        for _ in range(max_iter):
            vi_new = V_ind_hover**2 / np.sqrt((V * np.sin(alpha_T) + vi)**2 + (V * np.cos(alpha_T))**2)
            if abs(vi_new - vi) < tol:
                vi = vi_new
                break
            vi = vi_new
        P_vertical = Tvertical * vi * numberengines_vertical_MMA4
        P_horizontal = Thorizontal * V * numberengines_horizontal_MMA4
        P = (P_vertical + P_horizontal) / inputs[1]
    return P
