import numpy as np

def calculate_power_UFC_MMA_1(incline,V,rho, inputs, max_iter=1000, tol=1e-3):
    D = 0.5*rho*inputs[3]*inputs[2]*V**2
    Tvertical = np.cos(incline)*inputs[0]
    Thorizontal = D + np.sin(incline)*inputs[0]
    T = (Tvertical**2 + Thorizontal**2)**0.5
    alpha_T= np.cos(Tvertical/T)
    T_hover= inputs[0]
    V_ind_hover= (T_hover/(2*rho*inputs[4]))**0.5
    
    '''
    vi = V_ind_hover  # initial guess
    for _ in range(max_iter):
        vi_new = V_ind_hover**2 / np.sqrt((V * np.sin(alpha_T) + vi)**2 + (V * np.cos(alpha_T))**2)
        if abs(vi_new - vi) < tol:
            vi = vi_new
            break
        vi = vi_new
    ''' 
    vi= V_ind_hover/(1+V/V_ind_hover)**0.5
    P_induced = Tvertical * vi
    P_parasite = Thorizontal * V
    P = (P_induced + P_parasite) / inputs[1]
    
    #P = (abs(T)**3/(2*rho*inputs[4]))**0.5/inputs[1]
    return P


