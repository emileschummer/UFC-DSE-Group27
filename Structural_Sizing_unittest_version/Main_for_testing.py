import numpy as np
import matplotlib as plt
import pandas as pd

import os
import sys
target_folder = os.path.join(os.path.dirname(__file__), "..")
sys.path.append(os.path.abspath(target_folder))


from Structural_Sizing_unittest_version.InertiaCalcs import *
from Structural_Sizing_unittest_version.ForceAndStressCals import *
from Structural_Sizing_unittest_version.Materials import *
from Structural_Sizing_unittest_version.AirFoilDataExtraction import *

from scipy.integrate import quad


#------------------------------------------------------
#TODO ASK ALEX FOR FEEDBACK
#TODO CHECK VON MISES FOR ALL, ITS FOR CROSS SECTION POINT, NOT ENTIRE CROSS SECTION 
#------------------------------------------------------

class StructureModel:
    def __init__(self, Materials_Input, VTOL_Input, Tail_Input, Legs_Input, Wing_Input, Fuselage_Input, SF, BigG):
        self.Materials_Input = Materials_Input
        self.VTOL_Input = VTOL_Input
        self.Tail_Input = Tail_Input
        self.Legs_Input = Legs_Input
        self.Wing_Input = Wing_Input
        self.Fuselage_Input = Fuselage_Input
        self.SF = SF
        self.BigG = BigG
        self.init_materials()
        self.init_geometry()
        self.init_loads()

    def init_materials(self):
        mats = self.Materials_Input
        self.Material_VTOL = mats[0]
        self.Material_WingBox = mats[1]
        self.Material_Leg = mats[2]
        self.Material_Fuselage = mats[3]
        self.Material_Airfoil = mats[4]

    def init_geometry(self):
        self.MAC = self.Wing_Input[1]
        self.R_in_VTOL_front = self.VTOL_Input[0]
        self.R_out_VTOL_front = self.R_in_VTOL_front + (1/1000)
        self.d_prop = self.VTOL_Input[1]
        self.R_prop = self.d_prop / 2
        self.Vtol_Pole_Length_front = 1.1 * self.R_prop + 0.2 * self.MAC
        self.R_in_VTOL_back = self.VTOL_Input[0]
        self.R_out_VTOL_back = self.R_in_VTOL_back + (1/1000)
        self.Vtol_Pole_Length_back = 1.1 * self.R_prop + 0.8 * self.MAC
        self.Leg_Length = self.Legs_Input[0]
        self.R_leg = 1/1000
        self.R_in_fuselage = self.Fuselage_Input[0]
        self.R_out_fuselage = self.R_in_fuselage + 1/1000
        self.Fuselage_length_sec1 = self.Fuselage_Input[1]
        self.Fuselage_length_sec2 = self.Fuselage_Input[2]
        self.Fuselage_length_sec3 = self.Fuselage_Input[3]
        self.Payload_Location = self.Fuselage_Input[4] - self.Fuselage_length_sec1
        self.Wing_Hole_location = self.Fuselage_Input[5] - self.Fuselage_length_sec1 - self.Fuselage_length_sec2
        self.WingBox_length = self.Wing_Input[0] * 0.5
        self.R_out_WingBox = 0.5 * 0.12 * self.MAC
        self.R_in_WingBox = self.R_out_WingBox - 1/1000

    def init_loads(self):
        self.Safety_Factor = self.SF
        self.G_factor = self.BigG
        self.F_Vtol = self.VTOL_Input[2] * self.Safety_Factor
        self.T_Vtol = self.VTOL_Input[3] * self.Safety_Factor
        self.Tail_Effective_Length = self.Tail_Input[0]
        self.Entire_Tail_Length = self.Tail_Input[1]
        self.Tail_loading_horizontal_Distributed = self.Tail_Input[2] * self.Safety_Factor
        self.Tail_loading_Vertical_Distributed = self.Tail_Input[3] * self.Safety_Factor
        self.Leg_Force = ((self.Legs_Input[1] * 9.81 * self.G_factor) / 4) * self.Safety_Factor
        self.Main_Engine_Thrust = self.Fuselage_Input[6] * self.Safety_Factor
        self.Main_Engine_Torque = self.Fuselage_Input[7] * self.Safety_Factor
        self.Fuselage_Sec1_mass = self.Fuselage_Input[8]
        self.Fuselage_Sec2_mass = self.Fuselage_Input[9]
        self.Fuselage_Sec1_Load = (self.Fuselage_Sec1_mass * 9.81 * self.G_factor) / self.Fuselage_length_sec1 * self.Safety_Factor
        self.Fuselage_sec2_load = (self.Fuselage_Sec2_mass * 9.81 * self.G_factor) / self.Fuselage_length_sec2 * self.Safety_Factor
        self.Payload_Force = self.Fuselage_Input[10] * 9.81 * self.G_factor * self.Safety_Factor
        self.Payload_Drag = self.Fuselage_Input[11] * self.Safety_Factor
        self.Vtol_Location = 1.1 * self.R_prop
        self.Wing_Torque = self.Wing_Input[2]
        self.Wing_Lift_Distribution = self.Wing_Input[3]
        self.Wing_Total_Lift, self.Wing_Lift_Centroid_Location = Compute_Total_Lift_and_Centroid(self.Wing_Lift_Distribution, 0, self.WingBox_length)
        self.Wing_Total_Lift *= self.Safety_Factor
        self.Wing_Drag_Distribution = self.Wing_Input[4]
        self.Wing_Total_Drag, self.Wing_Drag_Centroid_Location = Compute_Total_Lift_and_Centroid(self.Wing_Drag_Distribution, 0, self.WingBox_length)
        self.Wing_MY = self.Wing_Total_Drag * self.Wing_Drag_Centroid_Location
        self.Wing_MZ = (self.Wing_Torque -
                        (self.F_Vtol * self.Vtol_Pole_Length_back + self.Tail_loading_Vertical_Distributed * self.Tail_Effective_Length * (self.Entire_Tail_Length - 0.5 * self.Tail_Effective_Length))
                        + (self.F_Vtol * self.Vtol_Pole_Length_front))
        self.Wing_MX = (-self.Vtol_Location * (2 * self.F_Vtol - self.Tail_Effective_Length * self.Tail_loading_Vertical_Distributed)
                        - self.Wing_Total_Lift * self.Wing_Lift_Centroid_Location)

    def optimize_vtol_front(self):
        while True:
            VTOL_I_Front = Circle_Moment_of_Inertia(self.R_out_VTOL_front, self.R_in_VTOL_front)
            VTOL_stress_Front = Bending(Mx=self.T_Vtol, Ix=VTOL_I_Front, X=self.R_out_VTOL_front,
                                        My=(self.F_Vtol * self.Vtol_Pole_Length_front), Iy=VTOL_I_Front, Y=self.R_out_VTOL_front)
            VTOL_Trans_Shear_Front = Shear_Transverse_Circle(R_in=self.R_in_VTOL_front, R_out=self.R_out_VTOL_front, F=self.F_Vtol)
            stress, shear = Von_Mises(Stress_X=0, Stress_Y=0, Stress_Z=VTOL_stress_Front, Shear_XY=VTOL_Trans_Shear_Front, Shear_YZ=0, Shear_ZX=0)
            if stress < self.Material_VTOL.Yield_Stress and shear < self.Material_VTOL.Yield_Shear:
                break
            self.R_out_VTOL_front += 0.001

    def optimize_vtol_back(self):
        while True:
            VTOL_I_Back = Circle_Moment_of_Inertia(self.R_out_VTOL_back, self.R_in_VTOL_back)
            VTOL_Trans_Shear_Back_Y = Shear_Transverse_Circle(R_in=self.R_in_VTOL_back, R_out=self.R_out_VTOL_back,
                                                              F=(self.F_Vtol + self.Tail_loading_Vertical_Distributed * self.Tail_Effective_Length))
            VTOL_Trans_Shear_Back_Z = Shear_Transverse_Circle(R_in=self.R_in_VTOL_back, R_out=self.R_out_VTOL_back,
                                                              F=self.Tail_Effective_Length * self.Tail_loading_horizontal_Distributed)
            VTOL_stress_Back = Bending(
                Mx=(self.T_Vtol + self.Tail_loading_horizontal_Distributed * self.Tail_Effective_Length * (self.Entire_Tail_Length - 0.5 * self.Tail_Effective_Length)),
                Ix=VTOL_I_Back, X=self.R_out_VTOL_back, Iy=VTOL_I_Back, Y=self.R_out_VTOL_back,
                My=(self.F_Vtol * self.Vtol_Pole_Length_back + self.Tail_loading_Vertical_Distributed * self.Tail_Effective_Length * (self.Entire_Tail_Length - 0.5 * self.Tail_Effective_Length)))
            stress, shear = Von_Mises(Stress_X=0, Stress_Y=0, Stress_Z=VTOL_stress_Back,
                                      Shear_XY=VTOL_Trans_Shear_Back_Y, Shear_YZ=VTOL_Trans_Shear_Back_Z, Shear_ZX=0)
            if stress < self.Material_VTOL.Yield_Stress and shear < self.Material_VTOL.Yield_Shear:
                break
            self.R_out_VTOL_back += 0.001

    def optimize_wingbox(self):
        while True:
            WingBox_t = self.R_out_WingBox - self.R_in_WingBox
            WingBox_I = Circle_Moment_of_Inertia(R_Out=self.R_out_WingBox, R_in=self.R_in_WingBox)
            WingBox_A = Tube_Area(R_in=self.R_in_WingBox, R_out=self.R_out_WingBox)
            WingBox_Bending_X = Bending_Simple(M=self.Wing_MX, Y=self.R_out_WingBox, I=WingBox_I)
            WingBox_Bending_Y = Bending_Simple(M=self.Wing_MY, Y=self.R_out_WingBox, I=WingBox_I)
            WingBox_Axial_Stress = (self.Tail_Effective_Length * self.Tail_loading_horizontal_Distributed) / WingBox_A
            WingBox_Torsion_Shear_Z = Shear_Circle_Torsion(T=self.Wing_MZ, r=self.R_out_WingBox, J=Circle_Polar_Moment_of_Inertia(R_out=self.R_out_WingBox, R_in=self.R_in_WingBox))
            WingBox_Transverse_Shear_Y = Shear_Transverse_Circle(R_in=self.R_in_WingBox, R_out=self.R_out_WingBox,
                                                                 F=(2 * self.F_Vtol - self.Tail_Effective_Length * self.Tail_loading_Vertical_Distributed + self.Wing_Total_Lift))
            WingBox_Transverse_Shear_X = Shear_Transverse_Circle(R_in=self.R_in_WingBox, R_out=self.R_out_WingBox, F=self.Wing_Total_Drag)
            Von_Mises_Wingbox_Stress, Von_Mises_Wingbox_Shear = Von_Mises(
                Stress_X=(WingBox_Bending_X + WingBox_Axial_Stress), Stress_Y=WingBox_Bending_Y, Stress_Z=0,
                Shear_XY=(WingBox_Torsion_Shear_Z + WingBox_Transverse_Shear_X + WingBox_Transverse_Shear_Y), Shear_YZ=0, Shear_ZX=0)
            WingBox_Buckle = Buckling_Stress(E=self.Material_WingBox.E, L=self.WingBox_length, A=WingBox_A, I=WingBox_I, K=2)
            # Deflection and twist checks omitted for brevity
            if (Von_Mises_Wingbox_Stress < self.Material_WingBox.Yield_Stress and
                WingBox_Axial_Stress < WingBox_Buckle and
                Von_Mises_Wingbox_Shear < self.Material_WingBox.Yield_Shear):
                break
            self.R_in_WingBox -= 0.001

    def optimize_leg(self):
        while True:
            Leg_A = (np.pi * self.R_leg ** 2)
            Leg_I = Solid_Circle_moment_of_Inertia(R=self.R_leg)
            Leg_Buckle = Buckling_Stress(E=self.Material_Leg.E, L=self.Leg_Length, I=Leg_I, A=Leg_A, K=2)
            Leg_Stress = self.Leg_Force / Leg_A
            if Leg_Stress < Leg_Buckle and Leg_Stress < self.Material_Leg.Yield_Stress:
                break
            self.R_leg += (1 / 1000)

    def optimize_fuselage(self):
        while True:
            # SECTION 1
            Fuselage_t = self.R_out_fuselage - self.R_in_fuselage
            Fuselage_J_sec1 = Circle_Polar_Moment_of_Inertia(R_out=self.R_out_fuselage, R_in=self.R_in_fuselage)
            Fuselage_I_sec1 = Circle_Moment_of_Inertia(R_Out=self.R_out_fuselage, R_in=self.R_in_fuselage)
            Fuselage_Torsion_Sec1 = Shear_Circle_Torsion(J=Fuselage_J_sec1, T=self.Main_Engine_Torque, r=self.R_out_fuselage)
            Fuselage_Buckle_sec1 = Buckling_Stress(E=self.Material_Fuselage.E, L=self.Fuselage_length_sec1, I=Fuselage_I_sec1, A=Tube_Area(R_out=self.R_out_fuselage, R_in=self.R_in_fuselage), K=2)
            Fuselage_Transverse_Shear_sec1 = Shear_Transverse_Circle(R_in=self.R_in_fuselage, R_out=self.R_out_fuselage, F=(self.Fuselage_Sec1_Load * self.Fuselage_length_sec1))
            Fuselage_Bending_Stress_sec1 = Bending_Simple(M=(-0.5 * self.Fuselage_Sec1_Load * (self.Fuselage_length_sec1 ** 2)), Y=self.R_out_fuselage, I=Fuselage_I_sec1)
            Fuselage_Axial_Stress_sec1 = self.Main_Engine_Thrust / Tube_Area(R_out=self.R_out_fuselage, R_in=self.R_in_fuselage)
            Fuselage_VonMises_Sec1_Stress, Fuselage_VonMises_Sec1_Shear = Von_Mises(
                Stress_X=Fuselage_Axial_Stress_sec1, Stress_Y=0, Stress_Z=Fuselage_Bending_Stress_sec1,
                Shear_XY=(Fuselage_Transverse_Shear_sec1 + Fuselage_Torsion_Sec1), Shear_YZ=0, Shear_ZX=0
            )

            # SECTION 2
            Fuselage_Sec1_Load_Total = self.Fuselage_Sec1_Load * self.Fuselage_length_sec1
            Fuselage_I_sec2 = Semi_Circle_Moment_of_Inertia(R_out=self.R_out_fuselage, R_in=self.R_in_fuselage)
            Fuselage_Torsion_Sec2 = Torsion_Open(T=self.Main_Engine_Torque, l=self.Fuselage_length_sec2, t=Fuselage_t)
            Fuselage_Buckle_sec2 = Buckling_Stress(E=self.Material_Fuselage.E, L=self.Fuselage_length_sec2, I=Fuselage_I_sec2, A=0.5 * Tube_Area(R_out=self.R_out_fuselage, R_in=self.R_in_fuselage), K=0.5)
            Fuselage_Transverse_Shear_sec2 = Shear_Transverse_General(
                F=(Fuselage_Sec1_Load_Total + self.Fuselage_length_sec2 * self.Fuselage_Sec1_Load + self.Payload_Force * self.Payload_Location),
                Q=First_Area_Q_SemiCircle(R_in=self.R_in_fuselage, R_out=self.R_out_fuselage, t=Fuselage_t),
                I=Fuselage_I_sec2, t=Fuselage_t
            )
            Fuselage_Bending_Stress_sec2 = Bending_Simple(
                M=-(Fuselage_Sec1_Load_Total + 0.5 * self.Fuselage_sec2_load * (self.Fuselage_length_sec2 ** 2)),
                Y=self.R_out_fuselage, I=Fuselage_I_sec2
            )
            Fuselage_Axial_Stress_sec2 = self.Main_Engine_Thrust / (0.5 * Tube_Area(R_out=self.R_out_fuselage, R_in=self.R_in_fuselage))
            Fuselage_VonMises_Sec2_Stress, Fuselage_VonMises_Sec2_Shear = Von_Mises(
                Stress_X=Fuselage_Axial_Stress_sec2, Stress_Y=0, Stress_Z=Fuselage_Bending_Stress_sec2,
                Shear_XY=(Fuselage_Transverse_Shear_sec2 + Fuselage_Torsion_Sec2), Shear_YZ=0, Shear_ZX=0
            )

            # SECTION 3
            Fuselage_Sec2_Load_Total = self.Fuselage_Sec1_Load * self.Fuselage_length_sec1 + self.Payload_Force + self.Fuselage_length_sec2 * self.Fuselage_sec2_load
            Fuselage_Sec3_X_Load = self.Main_Engine_Thrust - self.Payload_Drag
            Fuselage_J_sec3 = Circle_Polar_Moment_of_Inertia(R_out=self.R_out_fuselage, R_in=self.R_in_fuselage)
            Fuselage_I_sec3 = Circle_Moment_of_Inertia(R_Out=self.R_out_fuselage, R_in=self.R_in_fuselage)
            Cutout_Correction = Cut_Out_Corrections(Diamater=self.R_out_WingBox, Width=self.Fuselage_length_sec3)
            Fuselage_Torsion_Sec3 = Shear_Circle_Torsion(T=self.Main_Engine_Torque, r=self.R_out_fuselage, J=Fuselage_J_sec3)
            Fuselage_Buckle_sec3 = Buckling_Stress(E=self.Material_Fuselage.E, L=self.Fuselage_length_sec3, I=Fuselage_I_sec3, A=Tube_Area(R_out=self.R_out_fuselage, R_in=self.R_in_fuselage), K=2)
            Fuselage_Transverse_Shear_sec3 = Shear_Transverse_Circle(R_in=self.R_in_fuselage, R_out=self.R_out_fuselage, F=(self.Main_Engine_Thrust - self.Payload_Drag))
            Fuselage_Bending_Stress_sec3 = Bending_Simple(M=(Fuselage_Sec2_Load_Total * self.Wing_Hole_location), Y=self.R_out_fuselage, I=Fuselage_I_sec3)
            Fuselage_Axial_Stress_sec3 = self.Main_Engine_Thrust / Tube_Area(R_out=self.R_out_fuselage, R_in=self.R_in_fuselage)
            Fuselage_VonMises_Sec3_Stress, Fuselage_VonMises_Sec3_Shear = Von_Mises(
                Stress_X=(Cutout_Correction * Fuselage_Axial_Stress_sec3), Stress_Y=0,
                Stress_Z=Cutout_Correction * Fuselage_Bending_Stress_sec3,
                Shear_XY=Cutout_Correction * (Fuselage_Torsion_Sec3 + Fuselage_Transverse_Shear_sec3),
                Shear_YZ=0, Shear_ZX=0
            )

            # COMPARING
            if (Fuselage_VonMises_Sec1_Stress < self.Material_Fuselage.Yield_Stress and
                Fuselage_Axial_Stress_sec1 < Fuselage_Buckle_sec1 and
                Fuselage_VonMises_Sec1_Shear < self.Material_Fuselage.Yield_Shear):
                
                if (Fuselage_VonMises_Sec2_Stress < self.Material_Fuselage.Yield_Stress and
                    Fuselage_Axial_Stress_sec2 < Fuselage_Buckle_sec2 and
                    Fuselage_VonMises_Sec2_Shear < self.Material_Fuselage.Yield_Shear):
                    
                    if (Fuselage_VonMises_Sec3_Stress < self.Material_Fuselage.Yield_Stress and
                        Fuselage_Axial_Stress_sec3 < Fuselage_Buckle_sec3 and
                        Fuselage_VonMises_Sec3_Shear < self.Material_Fuselage.Yield_Shear):
                        # print("Passes Section 1,2,3")
                        break
                    else:
                        self.R_out_fuselage += 1 / 1000
                        # print("Passes Section 1,2")
                else:
                    self.R_out_fuselage += 1 / 1000
                    # print("Passes Section 1")
            else:
                self.R_out_fuselage += 1 / 1000

    def calculate_skin_mass(self):
        ScalingFactor_out = self.MAC / 1
        ScalingFactor_in = ScalingFactor_out * 0.995
        airfoil_file = os.path.join(os.path.dirname(__file__), "AirfoilData", "Airfoil.dat")
        Airfoil_Points = load_airfoil_dat(airfoil_file)
        _, _, _, Skin_Area_out = Airfoil_Moment_of_Inertia(Airfoil_Points, ScalingFactor_out)
        _, _, _, Skin_Area_in = Airfoil_Moment_of_Inertia(Airfoil_Points, ScalingFactor_in)
        Skin_Area = Skin_Area_out - Skin_Area_in
        Skin_mass = Skin_Area * self.WingBox_length * self.Material_Airfoil.Density
        return Skin_mass

    def calculate_vtol_pole_mass(self):
        Vtol_Pole_Mass_front = Volume(A=Tube_Area(R_out=self.R_out_VTOL_front, R_in=self.R_in_VTOL_front), L=self.Vtol_Pole_Length_front) * self.Material_VTOL.Density
        Vtol_Pole_Mass_back = Volume(A=Tube_Area(R_out=self.R_out_VTOL_back, R_in=self.R_in_VTOL_back), L=self.Entire_Tail_Length) * self.Material_VTOL.Density
        return 2 * (Vtol_Pole_Mass_front + Vtol_Pole_Mass_back)

    def calculate_fuselage_mass(self):
        return Volume(A=Tube_Area(R_in=self.R_in_fuselage, R_out=self.R_out_fuselage),
                      L=(self.Fuselage_length_sec2 + self.Fuselage_length_sec1 + self.Fuselage_length_sec3)) * self.Material_Fuselage.Density

    def calculate_leg_mass(self):
        return 4 * (self.Leg_Length * np.pi * self.R_leg ** 2) * self.Material_Leg.Density

    def calculate_wingbox_mass(self):
        return 2 * (Volume(A=Tube_Area(R_out=self.R_out_WingBox, R_in=self.R_in_WingBox), L=self.WingBox_length)) * self.Material_WingBox.Density

    def run(self):
        self.optimize_vtol_front()
        self.optimize_vtol_back()
        self.optimize_wingbox()
        self.optimize_leg()
        self.optimize_fuselage()
        Leg_Mass = self.calculate_leg_mass()
        Vtol_Pole_Mass = self.calculate_vtol_pole_mass()
        Fuselage_Mass = self.calculate_fuselage_mass()
        WingBox_Mass = self.calculate_wingbox_mass()
        Skin_mass = self.calculate_skin_mass()
        Structure_mass = Leg_Mass + Vtol_Pole_Mass + Fuselage_Mass + WingBox_Mass
        
        
        
        Total_Mass = Structure_mass + self.Fuselage_Sec1_mass + self.Fuselage_Sec2_mass + Skin_mass
        return Skin_mass, Leg_Mass, Vtol_Pole_Mass, WingBox_Mass, Fuselage_Mass, Structure_mass, Total_Mass

# if __name__ == "__main__":

#     Lift_Thing = lift_distribution_test
#     Drag_Thing = Drag_distribution_test
#     #RUN IT
#     model = StructureModel(Materials_Input=[DogshitTestMaterial(),Aluminum2024T4(),DogshitTestMaterial(),DogshitTestMaterial(),DogshitTestMaterial()],#BRAM MOLEST HERE 
#                 VTOL_Input=[0.01,0.736,70.6,2.28],
#                 Tail_Input=[0.15,3,20,30],
#                 Legs_Input=[0.25,25],
#                 Wing_Input=[3,0.65,18,Lift_Thing,Drag_Thing],
#                 Fuselage_Input=[0.125,0.1,0.3,0.4,0.4,0.6,150,10,2,5,0.8,10],
#                 SF=1.5,BigG=1.1)

#     result = model.run()
#     print("Skin Mass:", result[0])
#     print("Leg Mass:", result[1])
#     print("VTOL Pole Mass:", result[2])
#     print("Wing Box Mass:", result[3])
#     print("Fuselage Mass:", result[4])
#     print("Structure Mass:", result[5])
#     print("Total Mass:", result[6])

