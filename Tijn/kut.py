import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
#initial conditions

W = 200
m = W/9.81
piAe = 30
Clalpha = 4.635
Clhalpha = 4

CLmax = 2.4
CLmaxh = 1.8

Cl0 = 0.934
Clh0 = 0.1
b = 3
bh = 0.3

S = 1
Sh = 0.0607

rho = 1.2
Cd0 = 0.05
Cmac = -0.5
stall = (CLmax - Cl0)/Clalpha
V = 34
Vx = np.cos(stall)*V
Vz = np.sin(stall)*V

alpha = np.sin(Vz/V)

pitch = 0

pitchrate = 0


q = 0

lh = 2

l = 0.2
c = 0.36

Iy = 14

Cmalpha = 0
Tz = 0
Tx = 0
diff_thrust_pitch = 0

elevator_delta = 0

Cldelta = 0.5
Clhdelta = 0.5

def get_Cx():
    Cl = alpha*Clalpha + Cl0
    Cd = Cd0 + Cl**2/piAe
    Ct = np.cos(alpha)*Cd - np.sin(alpha)*Cl
    Cx = Tx/(0.5*rho*S*V**2) -np.sin(pitch)*W/(0.5*rho*S*V**2) - Ct
    return Cx

def get_Cz():
    Cl = alpha*Clalpha + Cl0
    Cd = Cd0 + Cl**2/piAe
    Clh = np.arcsin((lh*q + Vz)/V)*Clhalpha*(Sh/S) + Clh0*(Sh/S) + Clhdelta*elevator_delta*(Sh/S)
    Cn = np.cos(alpha)*Cl + np.sin(alpha)*Cd
    Cnh = np.cos(alpha)*Clh
    Cz = np.cos(pitch)*W/(0.5*rho*S*V**2) - Tz/(0.5*rho*S*V**2) - Cn - Cnh
    return Cz

def get_Cmy(): #pitch moment
    Cl = alpha*Clalpha + Cl0
    Cd = Cd0 + Cl**2/piAe
    Clh = ((Vz+lh*q)/V)*Clhalpha*(Sh/S) + Clh0*(Sh/S) + Clhdelta*elevator_delta*(Sh/S)
    Cn = np.cos(alpha)*Cl + np.sin(alpha)*Cd
    Cnh = np.cos(alpha)*Clh
    Cm = Cn*l/c + Cmac
    Cmh = -Cnh*lh/c
    Cmy = diff_thrust_pitch/(0.5*rho*S*c*V**2) + Cm + Cmh
    return Cmy

t = 0
tend = 100
dt = 0.01

velocity = []
AoA = []

pitchangle = []

time = []
X = 0
Z = 0
Xlst = []
Zlst = []
for Sh in np.linspace(0,1,300):
    V = 34
    Vx = np.cos(stall)*V
    Vz = np.sin(stall)*V
    alpha = np.arcsin(Vz/V)

    pitch = 0

    pitchrate = 0


    q = 0
    t = 0
    tend = 100
    dt = 0.01

    velocity = []
    AoA = []

    pitchangle = []

    time = []
    X = 0
    Z = 0
    Xlst = []
    Zlst = []

    while t < tend:

        t = t + dt
        if abs(pitch) < np.pi/2:
            Fx = 0.5*rho*S*V**2 * get_Cx()

            Fz = 0.5*rho*S*V**2 * get_Cz()

            My = 0.5*rho*S*c*V**2 * get_Cmy()
            Vx = Vx + dt*Fx/m

            Vz = Vz + dt*Fz/m

            q = q + dt*My/Iy #pitchrate
            pitch = pitch + dt*q
            V = (Vx**2 + Vz**2)**0.5
            alpha =  np.arcsin(Vz/V)

            pitchangle.append(pitch*180/np.pi)
            time.append(t)

    
    plt.plot(time,pitchangle)
    if abs(pitch) < np.pi/2:    
        print(Sh)
plt.show()



