import numpy as np
import matplotlib as plt
import pandas as pd
from InertiaCalcs import *
from ForceAndStressCals import *
from Materials import *
from AirFoilDataExtraction import *


#------------------------------------------------------
#TODO: ADD TRUSS STRUCTURE ANALYSIS FOR MAIN FRAME
#TODO: FIGURE OUT THE HINGE :(
#TODO: ASK DANIEL ABOUT WINGBOX ANALYSIS
#TODO: UUUUUHHHHHH, why do we not use the winglength?
#------------------------------------------------------

#Things to run
# Airfoil_Data = load_airfoil_dat("Structural Sizing\AirfoilData\Airfoil.dat")
# Airfoil_Data_Rotated = Rotate_for_Inertia(coordinates=Airfoil_Data, name= "s1223", angle= np.deg2rad(10))

# print(Airfoil_Moment_of_Inertia(Airfoil_Data,))
# print(Airfoil_Moment_of_Inertia(Airfoil_Data_Rotated))

Big_Owie_VTOL = False
Big_Owie_Tail = False
Big_owie_WingBox = True
MAC = 1


#Create the material
Material_Tail = AL()
Yield_shear_Tail= Material_Tail.Yield_Shear
Yield_Stress_Tail = Material_Tail.Yield_Stress
Density_Tail = Material_Tail.Density

Material_VTOL = AL()
Yield_shear_VTOL= Material_VTOL.Yield_Shear
Yield_Stress_VTOL = Material_VTOL.Yield_Stress
Density_VTOL = Material_VTOL.Density

Material_WingBox = AL()
Yield_shear_WingBox= Material_WingBox.Yield_Shear
Yield_Stress_WingBox = Material_WingBox.Yield_Stress
Density_WingBox = Material_WingBox.Density


#Loads
F_Vtol = 70.6 #25*9.81/4 #Newtons
F_prop = 100 #Newtons
T_Vtol = 2.28 #Newtons/Meter
T_prop = 1 #Newtons /Meter

Tail_loading_horizontal_Distributed = 20 #Newtons per meter
Tail_loading_Vertical_Distributed = 30 #Newtons per meter

WingBox_Torque = 100
WingBox_Lift_Distribution = 10 #Should be an elliptical func, we will figure it out later
WingBox_Max_Lift = 100
WingBox_Lift_at_VTOL = 75


#VTOL poles
R_in_VTOL = 0.03
R_out_VTOL = 0.035
Vtol_Pole_Length = 0.4
M_x = T_Vtol
M_y = F_Vtol*Vtol_Pole_Length


#TAIL
Tail_Length = 0.11 #Meters
Entire_Tail_Length = 1 #meters
Momenent_Acting_Point_Tail = Entire_Tail_Length - (Tail_Length*0.5)

Tail_Horizontal_Force = Tail_loading_horizontal_Distributed*Tail_Length
Tail_Vertical_Force = Tail_loading_Vertical_Distributed*Tail_Length

R_in_Tail = 0.01
R_out_Tail = 0.015

M_x_Tail = Tail_Horizontal_Force*Momenent_Acting_Point_Tail
M_y_Tail = Tail_Vertical_Force*Momenent_Acting_Point_Tail


#WINGBOX
Vtol_Location = 0.5 #along the wingbox
WingBox_B = 0.03
WingBox_H = 0.015
WingBox_t = 0.001
WingBox_length = 3



Failure_VTOL = False
#Sizing Time
while Failure_VTOL:
    Ix = Circle_Moment_of_Inertia(R_out_VTOL,R_in_VTOL)
    Iy=Ix
    VTOL_stress = Bending(M_x, Ix, R_out_VTOL, M_y, Iy, R_out_VTOL)
    VTOL_Trans_Shear = Shear_Transverse_Circle(R_in_VTOL,R_out_VTOL,F_Vtol)


    print("----------------------------------------------------")
    print("The Max Shear VTOL:",VTOL_stress, "The Yield Shear:", Yield_shear_VTOL)
    print("The Max Stress VTOL:",VTOL_Trans_Shear,"The yield stress", Yield_Stress_VTOL)
    print("The VTOL Thickness:",R_out_VTOL-R_in_VTOL)

    if VTOL_stress <= Yield_Stress_VTOL and VTOL_Trans_Shear <=Yield_shear_VTOL:
        Failure_VTOL = False
    else:
        R_out_VTOL +=0.001



while Big_Owie_Tail:
    Ix = Circle_Moment_of_Inertia(R_out_Tail,R_in_Tail)
    Iy = Ix

    Bending_Stress_Tail = Bending(M_x_Tail,Ix,R_out_Tail,M_y_Tail,Iy,R_out_Tail)
    Trans_Shear_Y_Tail = Shear_Transverse_Circle(R_in_Tail,R_out_Tail,Tail_Vertical_Force)
    Trans_Shear_x_Tail= Shear_Transverse_Circle(R_in_Tail,R_out_Tail,Tail_Horizontal_Force)

    Tail_Total_Shear = np.sqrt(Trans_Shear_x_Tail**2 + Trans_Shear_Y_Tail**2)

    print("----------------------------------------------------")
    print("The Max Shear WingBox:",Tail_Total_Shear, "The Yield Shear:", Yield_shear_Tail)
    print("The Max Stress Wingbox:",Bending_Stress_Tail,"The yield stress", Yield_Stress_Tail)
    print("Thickness Tail:",R_out_Tail-R_in_Tail)

    if Bending_Stress_Tail <= Yield_Stress_Tail and Tail_Total_Shear <=Yield_shear_Tail:
        Big_Owie_Tail = False
    else:
        R_out_Tail +=0.001





R_in_WingBox = 0.1
R_out_WingBox = 0.11

while Big_owie_WingBox:
    # WingBox_Ix = WingBox_Moment_of_inertia(B=WingBox_B,H=WingBox_H,t=WingBox_t)
    # WingBox_Iy = WingBox_Moment_of_inertia(B=WingBox_H,H=WingBox_B,t=WingBox_t)
    # WingBox_Q_x = First_Area_Q_WingBox(H=WingBox_H,B= WingBox_B, t= WingBox_t)
    # WingBox_Q_y = First_Area_Q_WingBox(H=WingBox_B,B= WingBox_H, t= WingBox_t)

    # WingBox_Torsion_Shear = Shear_Torsion(T=WingBox_Torque , t=WingBox_t , A=(WingBox_B*WingBox_H))

    
    # WingBox_Stress = Bending(Mx=(F_Vtol*Vtol_Location), Ix=WingBox_Ix, X=WingBox_B*0.5, My= (WingBox_Lift_at_VTOL*Vtol_Location), Iy=WingBox_Iy, Y=WingBox_H*0.5)

    # WingBox_Total_Shear = np.sqrt(WingBox_Torsion_Shear**2 + WingBox_Transverse_Shear_lift**2 + WingBox_Transverse_Shear_VTOL**2 )
    WingBox_Ix = Circle_Moment_of_Inertia(R_Out=R_out_WingBox,R_in=R_in_WingBox)
    WingBox_Iy = WingBox_Ix
    WingBox_Q = First_Area_Q_Circle(R_out=R_out_WingBox,R_in=R_in_WingBox,t=WingBox_t)
    WingBox_J = Circle_Polar_Moment_of_Inertia

    WingBox_Transverse_Shear_lift = Shear_Transverse_General(F = WingBox_Max_Lift, Q= WingBox_Q, I= WingBox_Ix, t=WingBox_t) #modelling for max shear, where force transfered from VTOl
    WingBox_Transverse_Shear_VTOL = Shear_Transverse_General(F = F_Vtol, Q= WingBox_Q, I= WingBox_Iy, t=WingBox_t)
    WingBox_Torsion_Shear = Shear_Circle_Torsion(T=WingBox_Torque, r=R_out_WingBox, J= WingBox_J)

    WingBox_Stress = Bending(Mx=1 ,Ix=WingBox_Ix, X= R_out_WingBox,My=1 ,Iy=WingBox_Iy,Y=R_out_WingBox) #FINISH ON FRIDAY

    print("----------------------------------------------------")
    print("The Max Shear WingBox:",WingBox_Total_Shear, "The Yield Shear:", Yield_shear_WingBox)
    print("The Max Stress Wingbox:",WingBox_Stress,"The yield stress", Yield_Stress_WingBox)
    print("The Wingbox Thickness:",WingBox_t)


    if WingBox_Total_Shear <= Yield_shear_WingBox and WingBox_Stress <= Yield_Stress_WingBox:
        Big_owie_WingBox = False
    else:
        WingBox_t +=0.001



Big_Owie_Leg = False
Required_Leg_Length_Front = 0.5


while Big_Owie_Leg:
    Big_Owie_Leg = False





#Calculate Mass
Tail_pole_mass = Volume(A=Tube_Area(R_out=R_out_Tail,R_in=R_in_Tail), L=Entire_Tail_Length)*Density_Tail
Vtol_Pole_Mass = Volume(A=Tube_Area(R_out=R_out_VTOL,R_in=R_in_VTOL), L=Vtol_Pole_Length)*Density_VTOL
WingBox_Mass = Volume(A=WingBox_Area(B=WingBox_B,H=WingBox_H,t=WingBox_t), L=WingBox_length)*Density_WingBox

TOTAL_MASS = 1*WingBox_Mass + 4*Vtol_Pole_Mass + 2*Tail_pole_mass
# print("Yippee")
# print("Yippee")
# print("Yippee")
# print("Yippee")
# print("Yippee")
# print(Tail_pole_mass)
# print(Vtol_Pole_Mass)
# print(WingBox_Mass)
# print(TOTAL_MASS)
# print("-------------------------------------------")
# print(R_in_VTOL,R_out_VTOL, (R_out_VTOL-R_in_VTOL))

