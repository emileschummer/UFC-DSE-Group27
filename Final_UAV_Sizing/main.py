#DSE Group 27 - UAV For Cycling
#import packages
import numpy as np
import os
#import functions
from Final_UAV_Sizing.Input.fixed_input_values import *
from Final_UAV_Sizing.Modelling.AerodynamicDesign.Functions import wing_geometry_calculator
from Final_UAV_Sizing.Modelling.AerodynamicDesign.AeroMain import run_full_aero


for number_relay_stations in range(1,6):
    M_init = 15 # kg
    M_final = 0
    while abs(M_init - M_final) >delta_mass:
#1. Wing Sizing
"""To begin with have to run in Functions wing_geometry_calculator to find S, ct and cr. (cannot get to save in csv results from AeroMain)
Then move on to AeroMain and run run_full_aero.
If you want the loading can then run on the output of run_full_aero called lift_distribution into load_distribution_halfspan form AerodynamicForces and get it for a specific alpha."""
    #1.1 Wing Geometry
        ##Prepare input values
        InputWeight = M_init
        alpha =
        csv = 
        velocity_op = V_stall*V_stall_safety_margin
        altitude =
        taper_ratio = 
        b = 
        ##Run
        S, cr, ct = wing_geometry_calculator(InputWeight, alpha, csv, velocity_op, altitude, taper_ratio, b)
    ##1.2 Aerodynamic Values
        ##Prepare input values
        airfoil_dat_path = os.path.join("Final_UAV_Sizing", "Input", "AirfoilData", "Airfoil.dat")
        name = "S1223"
        xfoil_path = r"C:\Users\marco\Downloads\xfoil\XFOIL6.99\xfoil.exe"
        operational_velocity = 10.0
        num_spanwise_sections = 200,
        vlm_chordwise_resolution = 6,
        delta_alpha_3D_correction = 1.0,
        alpha_range2D= np.linspace(-10, 25, 36),
        alpha_range3D = np.linspace(-10, 30, 41),
        r_chord = 0.35,
        t_chord = 0.35,
        r_twist = 0.0,
        t_twist = 0.0,
        sweep = 0.0,
        operational_altitude = 0.0,
        Re_numbers = 8,
        Plot = True,
        csv_path = "C:\\Users\\marco\\Documents\\GitHub\\UFC-DSE-Group27\\AerodynamicDesign\\aero.csv"
    
        ##Run
        """aero_values_dic={
        "wing_geom": wing_geom,
        "airplane_geom": airplane_geom,
        "CDs_vlm_original": CDs_vlm_original,
        "CLs_corrected": CLs_corrected,
        "lift_distribution": lift_distribution,
        "alphas" : alpha_range3D"""
        aero_values_dic = run_full_aero(airfoil_dat_path,name,xfoil_path,operational_velocity,num_spanwise_sections,vlm_chordwise_resolution,delta_alpha_3D_correction,alpha_range2D,alpha_range3D,r_chord,t_chord,r_twist,t_twist,sweep,operational_altitude,Re_numbers,Plot,csv_path)

#2. Propeller Sizing   
 T_props, Position of Props, No.Props	M_props, M_engines
#3. Battery Sizing
    


