

from DSE_strava import *
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'C:\\Users\\tijnp\\OneDrive\\Documenten\\Phyton\\DSE\\UFC-DSE-Group27\\Battery_Modelling')))
from Modelling.DSE_osprey import *

energy = 0
t = 0

for i in data:
    P = calculate_power(i[2],i[1],i[3])
    time = i[0]-t
    energy = energy + time*P
    t = i[0]
print(energy , 'J')
print(energy/3600 , 'Wh')