import numpy as np
numberengines_vertical_MMA4 = 4
numberengines_horizontal_MMA4 = 1


def calculate_power_UFC_MMA_4(incline,V,rho, inputs, max_iter=100, tol=1e-3):
    A = np.pi*(inputs[6]**2)/numberengines_vertical_MMA4 #m^2
    L = np.cos(incline)*inputs[0]
    if V >0:
        CL = 2*L/(rho*inputs[4]*V**2)
    else:
        CL = 10000#to jump into else statement
    if CL <= inputs[5]:
        CD = inputs[2] + CL**2/inputs[3]
        D = 0.5*rho*CD*inputs[4]*V**2
        T = (D + np.sin(incline)*inputs[0])
        P = T*V/inputs[1]
    else:
        CL = inputs[5]#np.sqrt(inputs[3]*inputs[2]) 
        CD = inputs[2] + CL**2/inputs[3]
        L = 0.5*rho*CL*inputs[4]*V**2 * inputs[7]  #parameter for wake of propellers
        D = 0.5*rho*CD*inputs[4]*V**2
        
        Tvertical = (np.cos(incline)*inputs[0] - L)/numberengines_vertical_MMA4
        Thorizontal = (D + np.sin(incline)*inputs[0])
        alpha_T= 0
        V_ind_hover= (Tvertical/(2*rho*A))**0.5
        
        
        vi = V_ind_hover  # initial guess
        for _ in range(max_iter):
            vi_new = V_ind_hover**2 / np.sqrt((V * np.sin(alpha_T) + vi)**2 + (V * np.cos(alpha_T))**2)
            if abs(vi_new - vi) < tol:
                vi = vi_new
                break
            vi = vi_new
        
        #vi= V_ind_hover/(1+V/V_ind_hover)**0.5
        P_vertical = Tvertical * vi * numberengines_vertical_MMA4
        P_horizontal = Thorizontal * V 
        P = (P_vertical + P_horizontal) / inputs[1]
    return P
