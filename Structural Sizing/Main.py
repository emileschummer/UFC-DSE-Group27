import numpy as np
import matplotlib as plt
import pandas as pd
from InertiaCalcs import *
from ForceAndStressCals import *
from Materials import *

#------------------------------------------------------
#TODO: ADD TRUSS STRUCTURE ANALYSIS FOR MAIN FRAME
#TODO: FIGURE OUT THE HINGE :(
#------------------------------------------------------
#Things to run
Big_Owie_VTOL = True
Big_Owie_Tail = True


#Loads
F_Vtol = 25*9.81/4 #Newtons
F_prop = 100 #Newtons
T_Vtol = 10 #Newtons/Meter
T_prop = 1 #Newtons /Meter
Wing_loading = 1 #Newtons per meter
Tail_loading_horizontal = 0.1 #Newtons per meter
Tail_loading_Vertical = 0.2 #Newtons per meter


#I beam
t1 = 2
t2 = 2
t3 = 2
H = 2
B = 2
L = 3

#Wing Box
t = 2
H = 1
B = 1
L = 1

#Tube
R_in = 0.05
R_out = 0.06
L = 2

#Solid block
B = 2
H = 2
L = 0.5



#VTOL poles
M_x = T_Vtol
M_y = F_Vtol*L

# Create an instance of the material
Material = DogshitTestMaterial()
Yield_shear= Material.Yield_Shear
Yield_Stress = Material.Yield_Stress

while Big_Owie_VTOL:
    print(R_out)
    Ix = Circle_Moment_of_Inertia(R_out,R_in)
    Iy=Ix
    B_stress = Bending(M_x, Ix, R_out, M_y, Iy, R_out)
    Trans_Shear = Shear_Transverse_Circle(R_in,R_out,F_Vtol)


    print("----------------------------------------------------")
    print("the Yield Stress is:",Yield_Stress)
    print("the current stress is:",B_stress)
    print("the Yield Shear is:",Yield_shear)
    print("the current Shear is:",Trans_Shear)
    print("IS SHE THICCC THO:",R_out)


    if B_stress <= Yield_Stress and Trans_Shear <=Yield_shear:
        Big_Owie = False
    else:
        R_out +=0.01




#TAIL
Tail_Length = 0.3 #Meters

