import all functions

delta_mass = 1 # kg, mass difference between initial and final mass
for number_relay_stations in range(1,6):
    M_init = 15 # kg
    M_final = 0
    V_stall = 6 # m/s
    while abs(M_init - M_final) >delta_mass:
        D_wing, L_wing, etc = WingSizing(M_init,V_stall)
        


