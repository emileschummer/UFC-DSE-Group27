import numpy as np
W = 200
max_thrust_vertical = 250
max_thrust_horizontal = 120
Clmax = 2.4
Cd0 = 0.05
piAe = 30
Cdmax = Cd0 + Clmax**2/piAe
rho = 1.225
S = 2
V = 0
velocity = []
inclination = []
while V < 120/3.6:
    L = 0.5*rho*S*Clmax*V**2
    D = 0.5*rho*S*Cdmax*V**2
    iv = np.arccos((L + max_thrust_vertical)/W)
    ih = np.arcsin((max_thrust_horizontal - D)/-W)
    print(iv)
    inclination.append(180*ih/np.pi)
    velocity.append(V)
    V = V + 0.5

import matplotlib.pyplot as plt
plt.plot(inclination,velocity)
plt.show()