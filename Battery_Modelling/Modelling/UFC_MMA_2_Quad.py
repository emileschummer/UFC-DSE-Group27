import numpy as np
numberengine_MMA2 = 4


def calculate_power_UFC_MMA_2(incline, V, rho, inputs, max_iter=100, tol=1e-3):
    S = inputs[3]*np.sin(incline) + inputs[4]*np.cos(incline)#inputs[3]*np.sin(inputs[1]) + inputs[4]*np.cos(inputs[1])
    D_profile = 0.5*rho*S*inputs[2]*V**2
    Tvertical = np.cos(incline)*inputs[0]/numberengine_MMA2
    Thorizontal = (D_profile + np.sin(incline)*inputs[0])/numberengine_MMA2
    T = (Tvertical**2 + Thorizontal**2)**0.5
    alpha_T= np.cos(Tvertical/T)
    #T_hover= inputs[0]/numberengine_MMA2
    A = inputs[5]/numberengine_MMA2
    V_ind_hover= (T/(2*rho*A))**0.5#(T_hover/(2*rho*A))**0.5

    vi = V_ind_hover  # initial guess
    for _ in range(max_iter):
        vi_new = V_ind_hover**2 / np.sqrt((V * np.sin(alpha_T) + vi)**2 + (V * np.cos(alpha_T))**2)
        if abs(vi_new - vi) < tol:
            vi = vi_new
            break
        vi = vi_new
    
    #vi= V_ind_hover/(1+V/V_ind_hover)**0.5
    P_induced = vi * numberengine_MMA2 *T#vertical
    P_parasite = 0#Thorizontal * V * numberengine_MMA2
    P = (P_induced + P_parasite) / inputs[1]
    
    
    #P = (abs(T)**3/(2*rho*A))**0.5*(numberengine_MMA2/inputs[1])
    return P

