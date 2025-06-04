import numpy as np
import matplotlib.pyplot as plt
Clalpha = 4.635
Clhalpha = 6
Cl0 = 0.934
Clh0 = 0.3
Cmac = -0.5
Cd0 = 0.05
piAe = 30
S = 1
Sh = 0.1
c = 0.36
l = 0.2
lh = 3
elevator_delta = [-30*np.pi/180,0,30*np.pi/180]
Clhdelta = 0.5
alpha = -20*np.pi/180

def get_Cmy(): #pitch moment
    Cl = alpha*Clalpha + Cl0
    Cd = Cd0 + Cl**2/piAe
    Clh = alpha*Clhalpha*(Sh/S) + Clh0*(Sh/S) + delta*Clhdelta*(Sh/S)
    Cn = np.cos(alpha)*Cl + np.sin(alpha)*Cd
    Cnh = np.cos(alpha)*Clh
    Cm = Cn*l/c + Cmac
    Cmh = -Cnh*lh/c
    Cmy = Cm + Cmh
    return Cmy

for delta in elevator_delta:
    AoA = []
    CM = []
    alpha = -20*np.pi/180
    while alpha < 25*np.pi/180:
        alpha = alpha + 0.001
        AoA.append(180*alpha/np.pi)
        CM.append(get_Cmy())

    plt.plot(AoA,CM)


    
plt.grid()

plt.show()