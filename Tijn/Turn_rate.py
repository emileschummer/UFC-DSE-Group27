import numpy as np
max_vertical_thrust = 280
max_diff_thrust_yaw = 50 #Nm
Clmax = 2.4
Sref = 2
W = 200
rho = 1.225
m = W/9.81

V = 5
turnrate = []
velocity = []
while V < 120/3.6:
    force = max_vertical_thrust + 0.5*rho*Sref*Clmax*V**2
    theta = np.arcsin(W/force)
    horizontal_force = np.cos(theta)*force
    r = m*V**2/horizontal_force
    omega = (horizontal_force/(m*r))**0.5
    velocity.append(V)
    turnrate.append(omega*180/np.pi)
    V = V +0.1
import matplotlib.pyplot as plt
plt.plot(velocity,turnrate)
plt.grid()
plt.xlabel("Velocity [m/s]")
plt.ylabel("Turn rate degree/s")
plt.show()
    