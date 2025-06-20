import numpy as np
import matplotlib as plt
import pandas as pd
from InertiaCalcs import *
from ForceAndStressCals import *
from Materials import *
from AirFoilDataExtraction import *
from scipy.integrate import quad

import os
from scipy.optimize import curve_fit

#------------------------------------------------------
#TODO ASK ALEX FOR FEEDBACK
#TODO CHECK VON MISES FOR ALL, ITS FOR CROSS SECTION POINT, NOT ENTIRE CROSS SECTION 
#------------------------------------------------------

def Structure_Main(Materials_Input,VTOL_Input,Tail_Input,Legs_Input,Wing_Input,Fuselage_Input,SF,BigG):
# def Structures_Main():
    #--------------------------------------------------
    #FUNCTIONS
    #--------------------------------------------------
    Big_owie_WingBox = True 
    Big_Owie_VTOL_front = True
    Big_Owie_VTOL_back = True
    Big_Owie_Fuselage_Flying = True
    Big_Owie_Leg = True
    MAC= Wing_Input[1] #0.64
    Safety_Factor = SF
    G_factor = BigG


    #--------------------------------------------------
    #MATERIALS BRAM EDIT HERE
    #--------------------------------------------------
    Material_VTOL = Aluminum7075T6() #Materials_Input[0] #AL()
    Yield_shear_VTOL= Material_VTOL.Yield_Shear
    Yield_Stress_VTOL = Material_VTOL.Yield_Stress
    Density_VTOL = Material_VTOL.Density

    Material_WingBox = Aluminum2024T4() #Materials_Input[1] #AL() 
    Yield_shear_WingBox= Material_WingBox.Yield_Shear
    Yield_Stress_WingBox = Material_WingBox.Yield_Stress
    Density_WingBox = Material_WingBox.Density

    Material_Leg = Aluminum2024T4() #Materials_Input[2] #AL() 
    Yield_shear_Leg = Material_Leg.Yield_Shear
    Yield_Stress_Leg = Material_Leg.Yield_Stress
    Density_Leg = Material_Leg.Density

    Material_Fuselage = NaturalFibre() #Materials_Input[3] #AL() 
    Yield_shear_Fuselage = Material_Fuselage.Yield_Shear
    Yield_Stress_Fuselage = Material_Fuselage.Yield_Stress
    Density_Fuselage = Material_Fuselage.Density

    Material_Airfoil = NaturalFibre() #Materials_Input[4] #PLA3DPrintMaterial()
    Density_Airfoil = Material_Airfoil.Density 


    #--------------------------------------------------
    #VTOL POLE ARMS
    #--------------------------------------------------
    R_in_VTOL_front = VTOL_Input[0]
    R_out_VTOL_front = R_in_VTOL_front+(1/1000)

    d_prop= VTOL_Input[1] #0.7366
    R_prop = d_prop/2	
    Vtol_Pole_Length_front = 1.1*R_prop + 0.2*MAC

    R_in_VTOL_back = VTOL_Input[0]
    R_out_VTOL_back = R_in_VTOL_back+(1/1000)
    Vtol_Pole_Length_back = 1.1*R_prop+ 0.8*MAC

    F_Vtol = VTOL_Input[2]*Safety_Factor ##Newtons 70.6
    T_Vtol = VTOL_Input[3]*Safety_Factor #Newtons/Meter 2.28


    #--------------------------------------------------
    #TAIL
    #--------------------------------------------------
    Tail_Effective_Length = Tail_Input[0] #Meters
    Entire_Tail_Length = Tail_Input[1] #meters NOTE THIS IS FROM WING BOX, SO INCLUDES THE VTOL POLE LENGTH

    Tail_loading_horizontal_Distributed = Tail_Input[2]*Safety_Factor #Newtons per meter
    Tail_loading_Vertical_Distributed = Tail_Input[3]*Safety_Factor #Newtons per meter


    #--------------------------------------------------
    #LEGS
    #--------------------------------------------------
    Leg_Length = Legs_Input[0]
    R_leg = 1/1000
    # Leg_Angle = np.deg2rad(30) #deg

    Leg_Force = ((Legs_Input[1]*9.81*G_factor)/4) *Safety_Factor
    # Leg_Force_X = Leg_Force*np.sin(Leg_Angle)
    # Leg_Force_Y = Leg_Force*np.cos(Leg_Angle)


    #--------------------------------------------------
    #FUSELAGE
    #--------------------------------------------------
    R_in_fuselage = Fuselage_Input[0] #(0.125)
    R_out_fuselage = R_in_fuselage+1/1000 

    Fuselage_length_sec1 = Fuselage_Input[1]
    Fuselage_length_sec2 = Fuselage_Input[2]
    Fuselage_length_sec3 = Fuselage_Input[3]

    Payload_Location = Fuselage_Input[4]-Fuselage_length_sec1 #edit the o.6 to the location, starting from the back of the fuselage ASSUMED MID SECTION
    Wing_Hole_location = Fuselage_Input[5]-Fuselage_length_sec1-Fuselage_length_sec2 #edit the 0.8, again measurong from the start of the back of the plane

    Main_Engine_Thrust = Fuselage_Input[6]*Safety_Factor #Newtons /Meter
    Main_Engine_Torque = Fuselage_Input[7]*Safety_Factor #Newtons /Meter

    Fuselage_Sec1_mass = Fuselage_Input[8]#1+0.5+0.4 *Safety_Factor #kg SENSORS +C OMSS +M AIN MOTOR
    Fuselage_Sec2_mass = Fuselage_Input[9]# 5 +0.7 *Safety_Factor #kg BATTERY+PARACHUTE

    Fuselage_Sec1_Load = (Fuselage_Sec1_mass*9.81*G_factor)/Fuselage_length_sec1 *Safety_Factor #N*m SENSORS +C OMSS +M AIN MOTOR (distributed load)
    Fuselage_sec2_load = (Fuselage_Sec2_mass*9.81*G_factor)/Fuselage_length_sec2 *Safety_Factor#N*m BATTERY+PARACHUTE
    Payload_Force = Fuselage_Input[10]*9.81*G_factor*Safety_Factor #N includes Gimbal and Camera weight
    Payload_Drag = Fuselage_Input[11]*Safety_Factor#N includes Gimbal and Camera drag


    #--------------------------------------------------
    #WINGBOX
    #--------------------------------------------------
    Vtol_Location = 1.1*R_prop #along the wingbox
    WingBox_length = Wing_Input[0]*0.5
    R_out_WingBox = 0.5*0.12*MAC
    R_in_WingBox = R_out_WingBox-1/1000

    Wing_Torque = Wing_Input[2] #MAX WING TORQUE
    Wing_Lift_Distribution = Wing_Input[3] #lift_distribution_test #lambda x: 1000 * (1 - (x/10)**2)  # Lift from root (x=0) to tip (x=10 m) #Should be an elliptical func, we will figure it out later REMEMBER -WL^2/2
    Wing_Total_Lift, Wing_Lift_Centroid_Location = Compute_Total_Lift_and_Centroid(Wing_Lift_Distribution,0,WingBox_length)
    Wing_Total_Lift=Wing_Total_Lift*Safety_Factor
    Wing_Drag_Distribution = Wing_Input[4]#Drag_distribution_test #(lambda x: 1000 * (1 - (x/10)**2))
    Wing_Total_Drag, Wing_Drag_Centroid_Location = Compute_Total_Lift_and_Centroid(Wing_Drag_Distribution,0,WingBox_length)


    #NEWLY DEFINED FROM VTOL
    Wing_MY= Wing_Total_Drag*Wing_Drag_Centroid_Location #Tail_Effective_Length*Tail_loading_horizontal_Distributed*(Entire_Tail_Length-0.5*Tail_Effective_Length) + Wing_Total_Drag*Wing_Drag_Centroid_Location
    Wing_MZ=( Wing_Torque -
                (F_Vtol*Vtol_Pole_Length_back+Tail_loading_Vertical_Distributed*Tail_Effective_Length*(Entire_Tail_Length-0.5*Tail_Effective_Length))
                + ( F_Vtol*Vtol_Pole_Length_front))
    Wing_MX = ( -Vtol_Location*(2*F_Vtol-Tail_Effective_Length*Tail_loading_Vertical_Distributed)
            -Wing_Total_Lift*Wing_Lift_Centroid_Location )



    #--------------------------------------------------
    #THE MODEL
    #--------------------------------------------------
    while Big_Owie_VTOL_front:
        VTOL_I_Front = Circle_Moment_of_Inertia(R_out_VTOL_front,R_in_VTOL_front)

        VTOL_stress_Front = Bending(Mx=(T_Vtol),Ix=VTOL_I_Front,X=R_out_VTOL_front,My=(F_Vtol*Vtol_Pole_Length_front),Iy=VTOL_I_Front,Y=R_out_VTOL_front)
        VTOL_Trans_Shear_Front = Shear_Transverse_Circle(R_in=R_in_VTOL_front,R_out=R_out_VTOL_front, F=F_Vtol)

        VTOL_VonMises_Front_Stress,VTOL_VonMises_Front_Shear = Von_Mises(Stress_X=0,Stress_Y=0,Stress_Z=VTOL_stress_Front,Shear_XY=(VTOL_Trans_Shear_Front),Shear_YZ=0,Shear_ZX=0)

        print("----------------------------------------------------")
        print("The Max Shear FRONT VTOL:",VTOL_VonMises_Front_Stress, "The Yield Shear:", Yield_shear_VTOL)
        print("The Max Stress FRONT VTOL:",VTOL_VonMises_Front_Shear,"The yield stress", Yield_Stress_VTOL)
        print("The FRONT VTOL Thickness:",R_out_VTOL_front-R_in_VTOL_front)

        if VTOL_VonMises_Front_Stress < Yield_Stress_VTOL and VTOL_VonMises_Front_Shear <Yield_shear_VTOL:
            Big_Owie_VTOL_front = False
        else:
            R_out_VTOL_front +=0.001




    while Big_Owie_VTOL_back:
        VTOL_I_Back = Circle_Moment_of_Inertia(R_out_VTOL_back,R_in_VTOL_back)
        VTOL_J_Back = Circle_Polar_Moment_of_Inertia(R_out=R_out_VTOL_back,R_in=R_in_VTOL_back)

        VTOL_Trans_Shear_Back_Y = Shear_Transverse_Circle(R_in=R_in_VTOL_back,R_out=R_out_VTOL_back,F=(F_Vtol+Tail_loading_Vertical_Distributed*Tail_Effective_Length))
        VTOL_Trans_Shear_Back_Z = Shear_Transverse_Circle(R_in=R_in_VTOL_back,R_out=R_out_VTOL_back,F=Tail_Effective_Length*Tail_loading_horizontal_Distributed)
        VTOL_stress_Back = Bending(Mx=(T_Vtol+Tail_loading_horizontal_Distributed*Tail_Effective_Length*(Entire_Tail_Length-0.5*Tail_Effective_Length))
                                    ,Ix=VTOL_I_Back,X=R_out_VTOL_back, Iy=VTOL_I_Back,Y=R_out_VTOL_back,
                                    My=(F_Vtol*Vtol_Pole_Length_back+Tail_loading_Vertical_Distributed*Tail_Effective_Length*(Entire_Tail_Length-0.5*Tail_Effective_Length)))

        VTOL_VonMises_Back_Stress,VTOL_VonMises_Back_Shear = Von_Mises(Stress_X=0,Stress_Y=0,Stress_Z=VTOL_stress_Back,
                                                                       Shear_XY=VTOL_Trans_Shear_Back_Y,Shear_YZ=VTOL_Trans_Shear_Back_Z,Shear_ZX=0)

        print("----------------------------------------------------")
        print("The Max Shear BACK VTOL:",VTOL_VonMises_Back_Stress, "The Yield Shear:", Yield_shear_VTOL)
        print("The Max Stress BACK VTOL:",VTOL_VonMises_Back_Shear,"The yield stress", Yield_Stress_VTOL)
        print("The BACK VTOL Thickness:",R_out_VTOL_back-R_in_VTOL_back)

        if VTOL_VonMises_Back_Stress < Yield_Stress_VTOL and VTOL_VonMises_Back_Shear <Yield_shear_VTOL:
            Big_Owie_VTOL_back = False
        else:
            R_out_VTOL_back +=0.001



    while Big_owie_WingBox:
        WingBox_t = R_out_WingBox - R_in_WingBox
        WingBox_I = Circle_Moment_of_Inertia(R_Out=R_out_WingBox,R_in=R_in_WingBox)
        WingBox_Q = First_Area_Q_Circle(R_out=R_out_WingBox,R_in=R_in_WingBox,t=WingBox_t)
        WingBox_J = Circle_Polar_Moment_of_Inertia(R_out=R_out_WingBox,R_in=R_in_WingBox)
        WingBox_J2 = Circle_Polar_Moment_of_Inertia2(t=WingBox_t, R_out=R_out_WingBox)# For comparison of thin walled
        WingBox_A = Tube_Area(R_in=R_in_WingBox,R_out=R_out_WingBox)

        #Bending
        WingBox_Bending_X = Bending_Simple(M=Wing_MX,Y=R_out_WingBox,I=WingBox_I)
        WingBox_Bending_Y = Bending_Simple(M=Wing_MY,Y=R_out_WingBox,I=WingBox_I)
        #WingBox_Bending_Z = Bending_Simple(M=Wing_MZ,Y=R_out_WingBox,I=WingBox_I)#TODO FIX THIS 
        WingBox_Axial_Stress = (Tail_Effective_Length*Tail_loading_horizontal_Distributed)/WingBox_A

        WingBox_Torsion_Shear_Z = Shear_Circle_Torsion(T=(Wing_MZ),r=R_out_WingBox,J=WingBox_J)
        WingBox_Transverse_Shear_Y = Shear_Transverse_Circle(R_in=R_in_WingBox,R_out=R_out_WingBox,
                                                        F=(2*F_Vtol-Tail_Effective_Length*Tail_loading_Vertical_Distributed + Wing_Total_Lift))  
        WingBox_Transverse_Shear_X  = Shear_Transverse_Circle(R_in=R_in_WingBox,R_out=R_out_WingBox,F=Wing_Total_Drag)                                                

        WingBox_Deflection_angle1 = Tip_Deflection_angle(F=(2*F_Vtol-Tail_Effective_Length*Tail_loading_Vertical_Distributed + Wing_Total_Lift),L=Wing_Lift_Centroid_Location,E=Material_WingBox.E,I=WingBox_I)
        WingBox_Deflection_angle2 = Tip_Deflection_angle(F=(2*F_Vtol-Tail_Effective_Length*Tail_loading_Vertical_Distributed),L=Vtol_Location,E=Material_WingBox.E,I=WingBox_I)
        WingBox_Deflection1 = Tip_Deflection(F=(2*F_Vtol-Tail_Effective_Length*Tail_loading_Vertical_Distributed + Wing_Total_Lift),
                                            L=Wing_Lift_Centroid_Location,
                                            E=Material_WingBox.E,I=WingBox_I)
        WingBox_Deflection2 = Tip_Deflection(F=(2*F_Vtol-Tail_Effective_Length*Tail_loading_Vertical_Distributed),
                                            L=Vtol_Location,
                                            E=Material_WingBox.E,I=WingBox_I)
        WingBox_Total_Deflection = WingBox_Deflection1+WingBox_Deflection2+WingBox_Deflection_angle2*(WingBox_length-Vtol_Location)
    
        WingBox_Twist_Angle = Twist(T = Wing_MZ,  L= WingBox_length, G=Material_WingBox.G, J=WingBox_J2)

        WingBox_Buckle = Buckling_Stress(E=Material_WingBox.E,L=WingBox_length, A=WingBox_A,I=WingBox_I,K=2)

        Von_Mises_Wingbox_Stress, Von_Mises_Wingbox_Shear = Von_Mises(Stress_X=(WingBox_Bending_X+WingBox_Axial_Stress),Stress_Y=WingBox_Bending_Y,Stress_Z=0,
                                                                    Shear_XY=(WingBox_Torsion_Shear_Z+WingBox_Transverse_Shear_X+WingBox_Transverse_Shear_Y), Shear_YZ=0,Shear_ZX=0)
        

        print("----------------------------------------------------")
        print("The Von Mises Stress Wingbox:",Von_Mises_Wingbox_Stress/(10**6),"The yield stress", Yield_Stress_WingBox/(10**6))
        print("The Von Mises Shear Wingbox:",Von_Mises_Wingbox_Shear/(10**6),"The yield stress", Yield_shear_WingBox/(10**6) )
        print("The Axial stress Wingbox:",WingBox_Axial_Stress/(10**6),"The Buckle stress", WingBox_Buckle/(10**6) )
        print("The Tip Deflection is:",WingBox_Total_Deflection, "And the Max allowable deflection is:",0.1*WingBox_length)
        print("The Twist Angle:", (WingBox_Twist_Angle), "And the allowable angle is:", 0.0174)
        print("The Wingbox Thickness:",R_out_WingBox, R_in_WingBox,R_out_WingBox - R_in_WingBox)
        WingBox_Twist_Angle = np.sqrt( WingBox_Twist_Angle**2 )
        WingBox_Total_Deflection = np.sqrt(WingBox_Total_Deflection**2)

        if (Von_Mises_Wingbox_Stress < Yield_Stress_WingBox and 
            WingBox_Axial_Stress < WingBox_Buckle and 
            Von_Mises_Wingbox_Shear < Yield_shear_WingBox and 
            WingBox_Total_Deflection < 0.1*WingBox_length and 
            (WingBox_Twist_Angle) < 0.0174532925):
            Big_owie_WingBox = False
        else:
            R_in_WingBox -=0.001



    while Big_Owie_Leg:
        # Leg_Ix = Circle_Moment_of_Inertia(R_Out=R_out_Leg,R_in=R_in_Leg)
        # Leg_Bending = Bending_Simple(M=(Leg_Length*Leg_Force_X), Y=R_out_Leg, I=Leg_Ix)
        # Leg_Transverse_Shear = Shear_Transverse_Circle(R_in=R_in_Leg,R_out=R_out_Leg,F=Leg_Force_X)
        # Leg_Von_Mises_Stress, Leg_Von_Mises_Shear = Von_Mises(Stress_X=Leg_Bending,Stress_Y=(Leg_Force_Y/Tube_Area(R_in=R_in_Leg,R_out=R_out_Leg)),Stress_Z=0,Shear_XY=Leg_Transverse_Shear,Shear_YZ=0,Shear_ZX=0)
        Leg_A = (np.pi*R_leg**2)
        Leg_I = Solid_Circle_moment_of_Inertia(R=R_leg)
        Leg_Buckle = Buckling_Stress(E=Material_Leg.E, L=Leg_Length,I=Leg_I,A=Leg_A,K=2)
        Leg_Stress = Leg_Force/Leg_A

        print("----------------------------------------------------")
        print("The Leg Stress:",Leg_Stress,"The buckle",Leg_Buckle, "The yield stress", Yield_Stress_Leg)
        print("The Leg:",R_leg)

        if Leg_Stress < Leg_Buckle and Leg_Stress < Yield_Stress_Leg:
            Big_Owie_Leg = False
        else:
            R_leg +=(1/1000)

    

    while Big_Owie_Fuselage_Flying:
        #SECTION 1:
        Fuselage_t = R_out_fuselage-R_in_fuselage
        

        Fuselage_J_sec1 = Circle_Polar_Moment_of_Inertia(R_out=R_out_fuselage,R_in=R_in_fuselage)
        Fuselage_I_sec1 = Circle_Moment_of_Inertia(R_Out=R_out_fuselage , R_in=R_in_fuselage)

        Fuselage_Torsion_Sec1 = Shear_Circle_Torsion(J=Fuselage_J_sec1, T= Main_Engine_Torque, r=R_out_fuselage)
        Fuselage_Buckle_sec1 = Buckling_Stress(E=Material_Fuselage.E, L= Fuselage_length_sec1, I=Fuselage_I_sec1, A=Tube_Area(R_out=R_out_fuselage,R_in=R_in_fuselage), K=2)
        Fuselage_Transverse_Shear_sec1 = Shear_Transverse_Circle(R_in=R_in_fuselage,R_out=R_out_fuselage,F=(Fuselage_Sec1_Load*Fuselage_length_sec1) ) #shear and therefore thickness would vary over the length of the beam, but modelling for worst case at joint where shear is max
        Fuselage_Bending_Stress_sec1 = Bending_Simple( M=(-0.5*Fuselage_Sec1_Load*(Fuselage_length_sec1**2)), Y=R_out_fuselage, I=Fuselage_I_sec1 )
        Fuselage_Axial_Stress_sec1 = Main_Engine_Thrust/Tube_Area(R_out=R_out_fuselage,R_in=R_in_fuselage)

        Fuselage_VonMises_Sec1_Stress, Fuselage_VonMises_Sec1_Shear = Von_Mises(Stress_X=Fuselage_Axial_Stress_sec1,Stress_Y=0,Stress_Z=Fuselage_Bending_Stress_sec1,Shear_XY=(Fuselage_Transverse_Shear_sec1+Fuselage_Torsion_Sec1),Shear_YZ=0, Shear_ZX=0)


        #SECTION 2:
        Fuselage_Sec1_Load_Total = Fuselage_Sec1_Load*Fuselage_length_sec1
        Fuselage_I_sec2 = Semi_Circle_Moment_of_Inertia(R_out=R_out_fuselage,R_in=R_in_fuselage)
        #Fuselage_I_sec2 = Semi_Circle_Moment_of_Inertia_Fuselage(R_out=R_out_fuselage,R_in=R_in_fuselage,t_Ibeam=Fuselage_t,B=0.02,H=0.02)

        Fuselage_Torsion_Sec2 = Torsion_Open(T=Main_Engine_Torque, l= Fuselage_length_sec2, t=Fuselage_t)
        Fuselage_Buckle_sec2 = Buckling_Stress(E=Material_Fuselage.E, L=Fuselage_length_sec2, I=Fuselage_I_sec2, A=0.5*Tube_Area(R_out=R_out_fuselage,R_in=R_in_fuselage), K=0.5)
        Fuselage_Transverse_Shear_sec2 = Shear_Transverse_General(F=(Fuselage_Sec1_Load_Total+Fuselage_length_sec2*Fuselage_Sec1_Load+Payload_Force*Payload_Location),Q=First_Area_Q_SemiCircle(R_in=R_in_fuselage,R_out=R_out_fuselage,t=Fuselage_t), I=Fuselage_I_sec2,t=Fuselage_t)  
        Fuselage_Bending_Stress_sec2 = Bending_Simple(M=-(Fuselage_Sec1_Load_Total+0.5*Fuselage_sec2_load*(Fuselage_length_sec2**2)), Y=R_out_fuselage,I=Fuselage_I_sec2)
        Fuselage_Axial_Stress_sec2 = Main_Engine_Thrust/(0.5*Tube_Area(R_out=R_out_fuselage,R_in=R_in_fuselage))

        
        Fuselage_VonMises_Sec2_Stress, Fuselage_VonMises_Sec2_Shear = Von_Mises(Stress_X=Fuselage_Axial_Stress_sec2,Stress_Y=0,Stress_Z=Fuselage_Bending_Stress_sec2,Shear_XY=(Fuselage_Transverse_Shear_sec2+Fuselage_Torsion_Sec2),Shear_YZ=0, Shear_ZX=0)


        #SECTION 3:
        Fuselage_Sec2_Load_Total = Fuselage_Sec1_Load*Fuselage_length_sec1+Payload_Force+Fuselage_length_sec2*Fuselage_sec2_load
        Fuselage_Sec3_X_Load = Main_Engine_Thrust-Payload_Drag

        Fuselage_J_sec3 = Circle_Polar_Moment_of_Inertia(R_out=R_out_fuselage,R_in=R_in_fuselage)
        Fuselage_I_sec3 = Circle_Moment_of_Inertia(R_Out=R_out_fuselage , R_in=R_in_fuselage)
        Cutout_Correction = Cut_Out_Corrections(Diamater=R_out_WingBox,Width=Fuselage_length_sec3)

        Fuselage_Torsion_Sec3 = Shear_Circle_Torsion(T=Main_Engine_Torque,r=R_out_fuselage,J=Fuselage_J_sec3)
        Fuselage_Buckle_sec3 = Buckling_Stress(E=Material_Fuselage.E, L=Fuselage_length_sec3, I= Fuselage_I_sec3, A=Tube_Area(R_out=R_out_fuselage,R_in=R_in_fuselage), K=2)
        Fuselage_Transverse_Shear_sec3 = Shear_Transverse_Circle(R_in=R_in_fuselage,R_out=R_out_fuselage,F=(Main_Engine_Thrust-Payload_Drag))
        Fuselage_Bending_Stress_sec3 = Bending_Simple(M=(Fuselage_Sec2_Load_Total*Wing_Hole_location),Y=R_out_fuselage,I=Fuselage_I_sec3) #Bending(Mx=(),Ix=Fuselage_I_sec3,X=R_out_fuselage,My=(),Iy=Fuselage_I_sec3,Y=R_out_fuselage)
        Fuselage_Axial_Stress_sec3 = Main_Engine_Thrust/Tube_Area(R_out=R_out_fuselage,R_in=R_in_fuselage)

        Fuselage_VonMises_Sec3_Stress, Fuselage_VonMises_Sec3_Shear = Von_Mises(Stress_X=(Cutout_Correction*Fuselage_Axial_Stress_sec3),Stress_Y=0, Stress_Z=Cutout_Correction*Fuselage_Bending_Stress_sec3, Shear_XY=Cutout_Correction*(Fuselage_Torsion_Sec3+Fuselage_Transverse_Shear_sec3),Shear_YZ=0,Shear_ZX=0 )
    
        print("-------------------------------------------")
        print("The Von Mises Stress Sec1:",Fuselage_VonMises_Sec1_Stress/(10**6),"The yield stress", Yield_Stress_Fuselage/(10**6))
        print("The Von Mises Shear Sec1:",Fuselage_VonMises_Sec1_Shear/(10**6),"The yield stress", Yield_shear_Fuselage/(10**6) )
        print("The Axial stress Sec1:",Fuselage_Axial_Stress_sec1/(10**6),"The Buckle stress", Fuselage_Buckle_sec1/(10**6) )
        print("-------------------------------------------")
        print("The Von Mises Stress Sec2:",Fuselage_VonMises_Sec2_Stress/(10**6),"The yield stress", Yield_Stress_Fuselage/(10**6))
        print("The Von Mises Shear Sec2:",Fuselage_VonMises_Sec2_Shear/(10**6),"The yield stress", Yield_shear_Fuselage/(10**6) )
        print("The Axial stress Sec2:",Fuselage_Axial_Stress_sec2/(10**6),"The Buckle stress", Fuselage_Buckle_sec1/(10**6) )
        print("-------------------------------------------")
        print("The Von Mises Stress Sec3:",Fuselage_VonMises_Sec3_Stress/(10**6),"The yield stress", Yield_Stress_Fuselage/(10**6))
        print("The Von Mises Shear Sec3:",Fuselage_VonMises_Sec3_Shear/(10**6),"The yield stress", Yield_shear_Fuselage/(10**6) )
        print("The Axial stress Sec3:",Fuselage_Axial_Stress_sec3/(10**6),"The Buckle stress", Fuselage_Buckle_sec1/(10**6) )
        
        print("-------------------------------------------")
        print("The Fuselage Thickness",R_out_fuselage,R_in_fuselage,R_out_fuselage-R_in_fuselage)


        #COMPARING
        print("-------------------------------------------")
        if (Fuselage_VonMises_Sec1_Stress < Yield_Stress_Fuselage and 
        Fuselage_Axial_Stress_sec1 < Fuselage_Buckle_sec1 and 
        Fuselage_VonMises_Sec1_Shear < Yield_shear_Fuselage):
            print("Passes Section 1")
            if (Fuselage_VonMises_Sec2_Stress < Yield_Stress_Fuselage and 
                Fuselage_Axial_Stress_sec2 < Fuselage_Buckle_sec2 and 
                Fuselage_VonMises_Sec2_Shear < Yield_shear_Fuselage):
                print("Passes Section 2")
                if (Fuselage_VonMises_Sec3_Stress < Yield_Stress_Fuselage and
                    Fuselage_Axial_Stress_sec3 < Fuselage_Buckle_sec3 and
                    Fuselage_VonMises_Sec3_Shear < Yield_shear_Fuselage):
                    print("Passes Section 3")
                    Big_Owie_Fuselage_Flying = False 
                else:
                    R_out_fuselage +=1/1000
                    Big_Owie_Fuselage_Flying = True 
            else:
                R_out_fuselage +=1/1000
                Big_Owie_Fuselage_Flying = True 
        else:
            R_out_fuselage +=1/1000
            Big_Owie_Fuselage_Flying = True 



    print("-------------------------------------------")
    ScalingFactor_out = MAC/1
    ScalingFactor_in =ScalingFactor_out*0.995

    Airfoil_Points = load_airfoil_dat("Structural Sizing\AirfoilData\Airfoil.dat")

    ##Bram: I used the lines below because loading the airfoil data didnt work for me without the os package:
    #airfoil_file = os.path.join(os.path.dirname(__file__), "AirfoilData", "Airfoil.dat")
    #Airfoil_Points = load_airfoil_dat(airfoil_file)
   
    _, _, _, Skin_Area_out = Airfoil_Moment_of_Inertia(Airfoil_Points, ScalingFactor_out)
    _, _, _, Skin_Area_in = Airfoil_Moment_of_Inertia(Airfoil_Points, ScalingFactor_in)
    Skin_Area = Skin_Area_out-Skin_Area_in
    Skin_mass = Skin_Area*WingBox_length*Density_Airfoil
    print("Wing Skin MASS:", Skin_mass)

    Vtol_Pole_Mass_front = Volume(A=Tube_Area(R_out=R_out_VTOL_front,R_in=R_in_VTOL_front), L=Vtol_Pole_Length_front)*Density_VTOL
    Vtol_Pole_Mass_back = Volume(A=Tube_Area(R_out=R_out_VTOL_back,R_in=R_in_VTOL_back), L=Entire_Tail_Length)*Density_VTOL
    Vtol_Pole_Mass = 2*(Vtol_Pole_Mass_front + Vtol_Pole_Mass_back)
    print("VTOL POLE MASS:", Vtol_Pole_Mass)

    Fuselage_Mass = Volume(A=Tube_Area(R_in=R_in_fuselage,R_out=R_out_fuselage), L=(Fuselage_length_sec2+Fuselage_length_sec1+Fuselage_length_sec3))*Density_Fuselage
    print('FUSELAGE MASS:', Fuselage_Mass)

    Leg_Mass = 4*(Leg_Length*np.pi*R_leg**2)*Density_Leg
    print("LEG MASS:", Leg_Mass)

    WingBox_Mass = 2*( Volume(A=Tube_Area(R_out=R_out_WingBox, R_in=R_in_WingBox), L=WingBox_length) )*Density_WingBox
    print("WingBox Mass", WingBox_Mass)


    Structure_mass = Leg_Mass+Vtol_Pole_Mass+Fuselage_Mass+WingBox_Mass+Skin_mass
    Total_Mass = Structure_mass+Fuselage_Sec1_mass+Fuselage_Sec2_mass + Skin_mass
    print("-------------------------------------------")
    print("THE STRUCTURE MASS:", Structure_mass)
    print("-------------------------------------------")
    print("-------------------------------------------")
    print("THE FINAL MASS:", Total_Mass)
    print("-------------------------------------------")

    Struc_mass_list = [Structure_mass,Leg_Mass,Vtol_Pole_Mass,WingBox_Mass,Skin_mass, Fuselage_Mass]
    Thickness_list = [R_out_VTOL_front-R_in_VTOL_front, R_out_VTOL_back-R_in_VTOL_back, R_out_WingBox-R_in_WingBox, R_out_fuselage-R_in_fuselage, R_leg]
    Materials_list = [Material_VTOL, Material_WingBox, Material_Leg, Material_Fuselage, Material_Airfoil]

    return Struc_mass_list, Thickness_list, Materials_list
# Elliptical lift distribution: cl(x) = cl_max * sqrt(1 - (x/b)^2)
# where x runs from -b/2 to b/2 (spanwise), or from 0 to b if only half-span

cl_values = np.array([
        1.93557809, 1.83327977, 1.93956023, 1.86539539, 1.91296618, 1.88956915,
        1.90549661, 1.90115547, 1.907348, 1.908479, 1.91220925, 1.91478053,
        1.91797211, 1.9209203, 1.92401692, 1.92706774, 1.93015375, 1.93323043,
        1.93631231, 1.939388, 1.9424587, 1.94552061, 1.94857269, 1.95161309,
        1.9546407, 1.95765435, 1.96065313, 1.96363623, 1.96660294, 1.96955265,
        1.97248483, 1.97539901, 1.97829476, 1.98117171, 1.98402952, 1.98686788,
        1.98968652, 1.99248517, 1.9952636, 1.99802157, 2.00075887, 2.0034753,
        2.00617065, 2.00884473, 2.01149736, 2.01412834, 2.01673748, 2.01932461,
        2.02188952, 2.02443204, 2.02695197, 2.0294491, 2.03192325, 2.0343742,
        2.03680175, 2.03920567, 2.04158574, 2.04394174, 2.04627342, 2.04858054,
        2.05086285, 2.05312008, 2.05535197, 2.05755823, 2.05973857, 2.06189269,
        2.06402029, 2.06612104, 2.0667922, 2.06631158, 2.06583096, 2.06535034,
        2.06486972, 2.0643891, 2.06390848, 2.06342786, 2.06294724, 2.06246661,
        2.06198599, 2.06150537, 2.06102475, 2.06054413, 2.06006351, 2.05958289,
        2.05910227, 2.05862165, 2.05814103, 2.05766041, 2.05717979, 2.05669916,
        2.05621854, 2.05573792, 2.0552573, 2.05477668, 2.05429606, 2.05381544,
        2.05333482, 2.0528542, 2.05237358, 2.05189296, 2.05141233, 2.05093171,
        2.05045109, 2.04997047, 2.04948985, 2.04900923, 2.04852861, 2.04804799,
        2.0475356, 2.04697523, 2.04641486, 2.04585449, 2.04529411, 2.04473374,
        2.04417337, 2.043613, 2.04305263, 2.04249225, 2.04193188, 2.04137151,
        2.04081114, 2.04025077, 2.03969039, 2.03913002, 2.03856965, 2.03800928,
        2.03744891, 2.03688853, 2.03632816, 2.03576779, 2.03520742, 2.03464705,
        2.03408667, 2.0335263, 2.03296593, 2.03240556, 2.03184519, 2.03128481,
        2.03072444, 2.03016407, 2.0296037, 2.02904333, 2.02848295, 2.02792258,
        2.02736221, 2.02721962, 2.02722944, 2.02723927, 2.02724909, 2.02725891,
        2.02726874, 2.02727856, 2.02728839, 2.02729821, 2.02730804, 2.02731786,
        2.02732769, 2.02708256, 2.02070366, 2.01400561, 2.00697298, 1.99958929,
        1.99183694, 1.98369714, 1.97514972, 1.9661731, 1.95674406, 1.94683765,
        1.93642697, 1.92548299, 1.91397429, 1.90186683, 1.88912362, 1.8757044,
        1.86156521, 1.84665792, 1.83092969, 1.81432236, 1.79677159, 1.77820606,
        1.75854629, 1.73770335, 1.71557723, 1.69205485, 1.66700753, 1.64028784,
        1.61172559, 1.58112252, 1.54824535, 1.51281638, 1.47450049, 1.43288606,
        1.38746043, 1.33755172, 1.28234897, 1.2202937, 1.15152066, 1.06339069,
        0.9975445, 0.78979516])

cl_distrib_max = cl_values
#cl_distrib_max = max_distrib[1]
#print(max_distrib)

# Assume these are at equally spaced spanwise stations from 0 to b/2
n = len(cl_distrib_max)
span = 3.1  # Example: total span = 3 m (adjust as needed)
y = np.linspace(0, span/2, n)  # y = 0 at root, y = b/2 at tip

# Fit cl_max to best match the data

def elliptical(y, cl_max):
    return cl_max * np.sqrt(1 - (y/(span/2))**2)

cl_max_fit, _ = curve_fit(elliptical, y, cl_distrib_max, p0=[2.0])

# Now you can use this function as the elliptical approximation:
def elliptical_cl(y):
    return cl_max_fit[0] * 1.225 * (20)**2 * np.sqrt(1 - (y/(span/2))**2)

def elliptical_cd(y):
    return 0.125 * elliptical_cl(y)

lift_distrib = elliptical_cl
drag_distrib = elliptical_cd

#Lift_Thing = lift_distribution_test
#Drag_Thing = Drag_distribution_test

Lift_Thing = lift_distrib
Drag_Thing = drag_distrib

# Example usage: elliptical_cl(y) for y in [0, span/2]
#RUN IT
Struc_mass_list, Thickness_list, Materials_list = Structure_Main(Materials_Input=[AL(),AL(),AL(),AL(),AL()],#BRAM MOLEST HERE 
               VTOL_Input=[0.01,0.736,70.6,2.28],
               Tail_Input=[0.15,3,20,30],
               Legs_Input=[0.25,25],
               Wing_Input=[3.1,0.65,18,Lift_Thing,Drag_Thing],
               Fuselage_Input=[0.125,0.1,0.3,0.4,0.4,0.6,150,10,2,5,0.8,10],
               SF=1.5,BigG=1.1)

M_struc, Leg_Mass,Vtol_Pole_Mass,WingBox_Mass,Skin_mass, Fuselage_Mass = Struc_mass_list  # Total Structure Mass
Thickness_Vtol_Pole_Front, Thickness_Vtol_Pole_Back, Thickness_WingBox, Thickness_Fuselage, Thickness_Legs = Thickness_list


print("Total Structure Mass:", M_struc)