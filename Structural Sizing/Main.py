import numpy as np
import matplotlib as plt
import pandas as pd
from InertiaCalcs import *
from ForceAndStressCals import *
from Materials import *
from AirFoilDataExtraction import *


#------------------------------------------------------
#TODO: ASK DANIEL ABOUT WINGBOX ANALYSIS
#TODO: UUUUUHHHHHH, why do we not use the winglength?
#------------------------------------------------------

#Things to run
# Airfoil_Data = load_airfoil_dat("Structural Sizing\AirfoilData\Airfoil.dat")
# Airfoil_Data_Rotated = Rotate_for_Inertia(coordinates=Airfoil_Data, name= "s1223", angle= np.deg2rad(10))

# print(Airfoil_Moment_of_Inertia(Airfoil_Data,))
# print(Airfoil_Moment_of_Inertia(Airfoil_Data_Rotated))

Big_Owie_VTOL = True
Big_Owie_Tail = True
Big_owie_WingBox = True
Big_Owie_VTOL_front = True
Big_Owie_VTOL_back = True
MAC = 1


#Create the material
Material_Tail = DogshitTestMaterial()
Yield_shear_Tail= Material_Tail.Yield_Shear
Yield_Stress_Tail = Material_Tail.Yield_Stress
Density_Tail = Material_Tail.Density

Material_VTOL = DogshitTestMaterial()
Yield_shear_VTOL= Material_VTOL.Yield_Shear
Yield_Stress_VTOL = Material_VTOL.Yield_Stress
Density_VTOL = Material_VTOL.Density

Material_WingBox = DogshitTestMaterial()
Yield_shear_WingBox= Material_WingBox.Yield_Shear
Yield_Stress_WingBox = Material_WingBox.Yield_Stress
Density_WingBox = Material_WingBox.Density

Material_Leg = DogshitTestMaterial()
Yield_shear_Leg = Material_Leg.Yield_Shear
Yield_Stress_Leg = Material_Leg.Yield_Stress
Density_Leg = Material_Leg.Density


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

Leg_Force = (25*9.81)/4


#VTOL poles front
R_in_VTOL_front = 0.17
R_out_VTOL_front = 0.1705
d_prop= 0.7366
R_prop = d_prop/2	
MAC= 0.35
Vtol_Pole_Length_front = 1.1*R_prop+ 0.12*MAC
M_y = F_Vtol*Vtol_Pole_Length_front
M_z = T_Vtol


#VTOL poles back
R_in_VTOL_back = 0.17
R_out_VTOL_back = 0.1705
d_prop= 0.7366
R_prop = d_prop/2	
MAC= 0.35
Vtol_Pole_Length_back = 1.1*R_prop+ 0.24*MAC
M_y = F_Vtol*Vtol_Pole_Length_front
M_z = T_Vtol





#Loads
F_Vtol = 61.3125 #25*9.81/4 #Newtons
F_prop = 100 #Newtons
T_Vtol = 2 #Newtons/Meter
T_prop = 1 #Newtons /Meter




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
WingBox_length = 1.5
M_x_WingBox = Vtol_Location*F_Vtol
M_y_WingBox = Vtol_Location*WingBox_Lift_at_VTOL
R_in_WingBox = 0.1
R_out_WingBox = 0.11



#Sizing Time
# while Failure_VTOL:
#     Ix = Circle_Moment_of_Inertia(R_out_VTOL,R_in_VTOL)
#     Iy=Ix
#     VTOL_stress = Bending(M_x, Ix, R_out_VTOL, M_y, Iy, R_out_VTOL)
#     VTOL_Trans_Shear = Shear_Transverse_Circle(R_in_VTOL,R_out_VTOL,F_Vtol)


#     print("----------------------------------------------------")
#     print("The Max Shear VTOL:",VTOL_stress, "The Yield Shear:", Yield_shear_VTOL)
#     print("The Max Stress VTOL:",VTOL_Trans_Shear,"The yield stress", Yield_Stress_VTOL)
#     print("The VTOL Thickness:",R_out_VTOL-R_in_VTOL)

#     if VTOL_stress <= Yield_Stress_VTOL and VTOL_Trans_Shear <=Yield_shear_VTOL:
#         Failure_VTOL = False
#     else:
#         R_out_VTOL +=0.001



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



while Big_owie_WingBox:
    # WingBox_Ix = WingBox_Moment_of_inertia(B=WingBox_B,H=WingBox_H,t=WingBox_t)
    # WingBox_Iy = WingBox_Moment_of_inertia(B=WingBox_H,H=WingBox_B,t=WingBox_t)
    # WingBox_Q_x = First_Area_Q_WingBox(H=WingBox_H,B= WingBox_B, t= WingBox_t)
    # WingBox_Q_y = First_Area_Q_WingBox(H=WingBox_B,B= WingBox_H, t= WingBox_t)
    # WingBox_Torsion_Shear = Shear_Torsion(T=WingBox_Torque , t=WingBox_t , A=(WingBox_B*WingBox_H))
    # WingBox_Stress = Bending(Mx=(F_Vtol*Vtol_Location), Ix=WingBox_Ix, X=WingBox_B*0.5, My= (WingBox_Lift_at_VTOL*Vtol_Location), Iy=WingBox_Iy, Y=WingBox_H*0.5)
    # WingBox_Total_Shear = np.sqrt(WingBox_Torsion_Shear**2 + WingBox_Transverse_Shear_lift**2 + WingBox_Transverse_Shear_VTOL**2 )
    WingBox_t = R_out_WingBox - R_in_WingBox

    WingBox_Ix = Circle_Moment_of_Inertia(R_Out=R_out_WingBox,R_in=R_in_WingBox)
    WingBox_Iy = WingBox_Ix
    WingBox_Q = First_Area_Q_Circle(R_out=R_out_WingBox,R_in=R_in_WingBox,t=WingBox_t)
    WingBox_J = Circle_Polar_Moment_of_Inertia(R_out=R_out_WingBox,R_in=R_in_WingBox)

    WingBox_Transverse_Shear_lift = Shear_Transverse_General(F = WingBox_Max_Lift, Q= WingBox_Q, I= WingBox_Ix, t=WingBox_t) #modelling for max shear, where force transfered from VTOl
    #WingBox_Transverse_Shear_VTOL = Shear_Transverse_General(F = F_Vtol, Q= WingBox_Q, I= WingBox_Iy, t=WingBox_t) # ASSUMING EQUAL DUE TO DOUBLE POLES
    WingBox_Torsion_Shear = Shear_Circle_Torsion(T=WingBox_Torque, r=R_out_WingBox, J= WingBox_J)

    WingBox_Stress = Bending(Mx=M_x_WingBox ,Ix=WingBox_Ix, X= R_out_WingBox,My=M_y_WingBox ,Iy=WingBox_Iy,Y=R_out_WingBox) 
    WingBox_Total_Shear = WingBox_Torsion_Shear+WingBox_Transverse_Shear_lift

    Tresca_Stress_Wingbox = Tresca(Stress1=WingBox_Stress,Stress2=0,Shear=WingBox_Total_Shear)
    Von_Mises_Wingbox_Stress, Von_Mises_Wingbox_Shear = Von_Mises(Stress_X=WingBox_Stress,Stress_Y=0,Stress_Z=0,Shear_XY=WingBox_Total_Shear,Shear_YZ=0,Shear_ZX=0)
    
    WingBox_Deflection = Tip_Deflection(F=WingBox_Lift_Distribution,L=WingBox_length,E=Material_WingBox.E,I=WingBox_Ix)
    WingBox_Twist_Angle = Twist(T = WingBox_Torque,  L= WingBox_length, G=Material_WingBox.G, J=WingBox_J)


    print("----------------------------------------------------")
    print("The Tresca Stress WingBox:",Tresca_Stress_Wingbox, "The Yield Shear:",Yield_Stress_WingBox)
    print("The Von Mises Stress Wingbox:",Von_Mises_Wingbox_Stress,"The yield stress", Yield_Stress_WingBox)
    print("The Von Mises Shear Wingbox:",Von_Mises_Wingbox_Shear,"The yield stress", Yield_shear_WingBox )
    print("The Wingbox Thickness:",WingBox_t)


    if Tresca_Stress_Wingbox < Yield_Stress_WingBox and Von_Mises_Wingbox_Stress < Yield_Stress_WingBox and Von_Mises_Wingbox_Shear < Yield_Stress_WingBox and WingBox_Deflection < 0.05*WingBox_length:
        Big_owie_WingBox = False
    else:
        R_out_WingBox +=0.001



Big_Owie_Leg = False
Leg_Length = 0.5
R_in_Leg= 1/1000
R_out_Leg = 2/1000
Leg_Angle = np.deg2rad(30) #deg
Leg_Force_X = Leg_Force*np.sin(Leg_Angle)
Leg_Force_Y = Leg_Force*np.cos(Leg_Angle)



while Big_Owie_Leg:
    Leg_Ix = Circle_Moment_of_Inertia(R_Out=R_out_Leg,R_in=R_in_Leg)

    Leg_Bending = Bending_Simple(M=(Leg_Length*Leg_Force_X), Y=R_out_Leg, I=Leg_Ix)
    Leg_Transverse_Shear = Shear_Transverse_Circle(R_in=R_in_Leg,R_out=R_out_Leg,F=Leg_Force_X)

    Leg_Buckle = Buckling_Stress(E=Material_Leg.E, L=Leg_Length,I=Leg_Ix,A=Tube_Area(R_out=R_out_Leg,R_in=R_in_Leg),K=2)

    Leg_Von_Mises_Stress, Leg_Von_Mises_Shear = Von_Mises(Stress_X=Leg_Bending,Stress_Y=Leg_Buckle,Stress_Z=0,Shear_XY=Leg_Transverse_Shear,Shear_YZ=0,Shear_ZX=0)

    
    print("----------------------------------------------------")
    print("The Von Mises Stress Leg:",Leg_Von_Mises_Stress,"The yield stress", Yield_Stress_Leg)
    print("The Von Mises Shear Leg:",Leg_Von_Mises_Shear,"The yield stress", Yield_shear_Leg)
    print("The Wingbox Leg:",R_out_Leg-R_in_Leg)

    if Leg_Von_Mises_Stress < Yield_Stress_Leg and Leg_Von_Mises_Shear < Yield_shear_Leg:
        Big_Owie_Leg = False
    else:
        R_out_Leg +=(1/1000)



while Big_Owie_VTOL_front:
    Iy = Circle_Moment_of_Inertia(R_out_VTOL_front,R_in_VTOL_front)
    Iz=Iy
    VTOL_stress = Bending(M_y, Iy, R_out_VTOL_front, M_z, Iz, R_out_VTOL_front)
    VTOL_Trans_Shear = Shear_Transverse_Circle(R_in_VTOL_front,R_out_VTOL_front,F_Vtol)


    print("----------------------------------------------------")
    print("The Max Shear FRONT VTOL:",VTOL_stress, "The Yield Shear:", Yield_shear_VTOL)
    print("The Max Stress FRONT VTOL:",VTOL_Trans_Shear,"The yield stress", Yield_Stress_VTOL)
    print("The FRONT VTOL Thickness:",R_out_VTOL_front-R_in_VTOL_front)

    if VTOL_stress <= Yield_Stress_VTOL and VTOL_Trans_Shear <=Yield_shear_VTOL:
        Big_Owie_VTOL_front = False
    else:
        R_out_VTOL_front +=0.001



while Big_Owie_VTOL_back:
    Iy = Circle_Moment_of_Inertia(R_out_VTOL_back,R_in_VTOL_back)
    Iz=Iy
    VTOL_stress = Bending(M_y, Iy, R_out_VTOL_back, M_z, Iz, R_out_VTOL_back)
    VTOL_Trans_Shear = Shear_Transverse_Circle(R_in_VTOL_back,R_out_VTOL_back,F_Vtol)


    print("----------------------------------------------------")
    print("The Max Shear BACK VTOL:",VTOL_stress, "The Yield Shear:", Yield_shear_VTOL)
    print("The Max Stress BACK VTOL:",VTOL_Trans_Shear,"The yield stress", Yield_Stress_VTOL)
    print("The BACK VTOL Thickness:",R_out_VTOL_back-R_in_VTOL_back)

    if VTOL_stress <= Yield_Stress_VTOL and VTOL_Trans_Shear <=Yield_shear_VTOL:
        Big_Owie_VTOL_back = False
    else:
        R_out_VTOL_back +=0.001



Big_Owie_Fuselage_Flying = True

R_out_VTOL_fuselage = 0.3
R_in_VTOL_fusolage = 0.3+1/1000

while Big_Owie_Fuselage_Flying:
    Fuselage_Full_Section_J = Circle_Polar_Moment_of_Inertia(R_out_VTOL_fuselage, R_in_VTOL_fusolage)
    VTOL_stress = Shear_Circle_Torsion(T_prop,R_out_VTOL_fuselage,Fuselage_Full_Section_J)
    

    Big_Owie_Fuselage_Flying = False #just here so you dont get an infinite loop error










#Calculate Mass
Tail_pole_mass = Volume(A=Tube_Area(R_out=R_out_Tail,R_in=R_in_Tail), L=Entire_Tail_Length)*Density_Tail
WingBox_Mass = Volume(A=Tube_Area(R_out=R_out_WingBox,R_in=R_in_WingBox), L=WingBox_length)*Density_WingBox

Vtol_Pole_Mass_front = Volume(A=Tube_Area(R_out=R_out_VTOL_front,R_in=R_in_VTOL_front), L=Vtol_Pole_Length_front)*Density_VTOL
Vtol_Pole_Mass_back = Volume(A=Tube_Area(R_out=R_out_VTOL_back,R_in=R_in_VTOL_back), L=Vtol_Pole_Length_back)*Density_VTOL

Vtol_Pole_Mass = Vtol_Pole_Mass_front + Vtol_Pole_Mass_back
print("VTOL Pole Mass:", Vtol_Pole_Mass)

TOTAL_MASS = 2*WingBox_Mass + 4*Vtol_Pole_Mass + 2*Tail_pole_mass
print("Yippee")
print("Yippee")
print("Yippee")
print("Yippee")
print("Yippee")
print(Tail_pole_mass)
print(Vtol_Pole_Mass)
print(WingBox_Mass)
print(TOTAL_MASS)
print("-------------------------------------------")
print(R_in_VTOL,R_out_VTOL, (R_out_VTOL-R_in_VTOL))

