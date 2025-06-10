import numpy as np
import matplotlib.pyplot as plt
Clalpha = 4.635
Clhalpha = 4.158
W = 200
Cl0 = 1.6
Clh0 = -0.3
Clmax = 2.4
clhmax = 1.7
Cmac = -0.5
Cd0 = 0.05
piAe = 30
S = 1
Sh = 0.25
c = 0.36
l = 0.0146
lh = l + 1
rho = 1.225
elevator_delta = [-30*np.pi/180,0,30*np.pi/180]
Clhdelta = 1.5
alpha = -20*np.pi/180
max_diff_pitch_thrust = 100 #[Nm]
Vstall = (W/(0.5*rho*S*Clmax))**0.5
Vmax = 120/3.6
Velocities = np.linspace(Vstall,Vmax,100)
AoA1 = []
for V in Velocities:
    AoA1.append((((W/(0.5*S*rho*V**2))-Cl0)/Clalpha)*180/np.pi)

plt.plot(AoA1,Velocities)
plt.grid()
plt.show()
print('minimum angle of attack is' + str(min(AoA1)) + 'mamximum angle of attack is' + str(max(AoA1)))

for alpha in AoA1:
    Cl = alpha*Clalpha + Cl0
    Cd = Cd0 + Cl**2/piAe
    Cn = np.cos(alpha)*Cl + np.sin(alpha)*Cd
    Cm = Cn*l/c + Cmac
    M = 0.5*rho*S*c*Cmac*Vmax**2
    Ftail = M/lh



def get_Cmy(): #pitch moment
    Cl = alpha*Clalpha + Cl0
    Cd = Cd0 + Cl**2/piAe
    Clh = alpha*Clhalpha*(Sh/S) + Clh0*(Sh/S) + delta*Clhdelta*(Sh/S)
    if abs(Cl) < Clmax:
        Cn = np.cos(alpha)*Cl + np.sin(alpha)*Cd
    else:
        Cn = 0
    if abs(Clh) < clhmax*(Sh/S):
        Cnh = np.cos(alpha)*Clh
    else:
        Cnh = 0
    Cm = Cn*l/c + Cmac
    Cmh = -Cnh*lh/c
    Cmy = Cm + Cmh
    return Cmy




for delta in elevator_delta:
    AoA = []
    CM = []
    alpha = -45*np.pi/180
    while alpha < 45*np.pi/180:
        alpha = alpha + 0.001
        AoA.append(180*alpha/np.pi)
        CM.append(get_Cmy())

    plt.plot(AoA,CM)

plt.plot([min(AoA1),max(AoA1)],[0,0])
    
plt.grid()

plt.show()

max_tail_froce = 0.5*rho*S*c*Cmac*Vmax**2
print(max_tail_froce)