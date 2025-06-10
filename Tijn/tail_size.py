import numpy as np
import matplotlib.pyplot as plt
Clvbeta = 4.158
Clvmax = 1.5
Sv = 0.1
lv = 1
Iz = 23
Vy = 5
V = 30
roll = 0*np.pi/180
r = 0 #yawrate
W = 200
m = 200/9.81
rho = 1.225
t = 0
tend = 60
dt = 0.01
sideslip = []
time = []
while t < tend:
    t = t + dt
    beta = np.arcsin((Vy - lv*r)/V)
    Fy = -0.5*rho*Sv*V**2 * beta * Clvbeta + np.sin(roll)*W
    Mz = Fy * lv
    Vy = Vy + dt*Fy/m
    r = r + dt*Mz/Iz
    sideslip.append(180*beta/np.pi)
    time.append(t)

plt.plot(time,sideslip)
plt.show()