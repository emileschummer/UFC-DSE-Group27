import numpy as np

T = 11.1893
L = 1.5
Theta = np.deg2rad(1)
G=1.3e9
d = 2*0.384

t = (T*L*4)/(Theta*G*np.pi*d**3)
print(t)