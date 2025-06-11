#DSE Group 27 - UAV For Cycling
#import packages
import numpy as np
import os
import pandas as pd
#import functions
import Final_UAV_Sizing.Input.fixed_input_values as input
from Final_UAV_Sizing.Modelling.AerodynamicDesign.Functions import wing_geometry_calculator
from Final_UAV_Sizing.Modelling.AerodynamicDesign.AeroMain import run_full_aero
from Final_UAV_Sizing.Modelling.Propeller_and_Battery_Sizing.Model.Battery_modelling import Battery_Model, Battery_Size



for number_relay_stations in range(1,input.max_RS):
    M_init = input.M_init
    M_final = 0
    while abs(M_init - M_final) > input.delta_mass:
#0. Open General Files
        aero_df = pd.read_csv(input.aero_csv)
#1. Wing Sizing
"""To begin with have to run in Functions wing_geometry_calculator to find S, ct and cr. (cannot get to save in csv results from AeroMain)
Then move on to AeroMain and run run_full_aero.
If you want the loading can then run on the output of run_full_aero called lift_distribution into load_distribution_halfspan form AerodynamicForces and get it for a specific alpha."""
    #1.1 Wing Geometry
        ##Prepare input values
        InputWeight = M_init
        aero_df = aero_df
        velocity_op = input.V_stall*input.V_stall_safety_margin
        altitude = input.altitude
        taper_ratio = input.taper_ratio
        b = input.b
        ##Run
        S_mw, cr, ct = wing_geometry_calculator(InputWeight, aero_df, velocity_op, altitude, taper_ratio, b)
    ##1.2 Aerodynamic Values
        ##Prepare input values
        airfoil_dat_path = os.path.join("Final_UAV_Sizing", "Input", "AirfoilData", "Airfoil.dat")
        name = "S1223"
        xfoil_path = input.xfoil
        operational_velocity = input.V_stall*input.V_stall_safety_margin
        num_spanwise_sections = input.num_spanwise_sections,
        vlm_chordwise_resolution = input.vlm_chordwise_resolution,
        delta_alpha_3D_correction = input.delta_alpha_3D_correction,
        alpha_range2D= input.alpha_range2D,
        alpha_range3D = input.alpha_range3D,
        r_chord = cr,
        t_chord = ct,
        r_twist = input.r_twist,
        t_twist = input.t_twist,
        sweep = input.sweep,
        operational_altitude = input.altitude,
        Re_numbers = input.Re_numbers,
        Plot = input.show_plots,
        csv_path = input.aero_csv
        ##Run
        """aero_values_dic={
        "wing_geom": wing_geom,
        "airplane_geom": airplane_geom,
        "CDs_vlm_original": CDs_vlm_original,
        "CLs_corrected": CLs_corrected,
        "lift_distribution": lift_distribution,
        "alphas" : alpha_range3D"""
        aero_values_dic = run_full_aero(airfoil_dat_path,name,xfoil_path,operational_velocity,num_spanwise_sections,vlm_chordwise_resolution,delta_alpha_3D_correction,alpha_range2D,alpha_range3D,r_chord,t_chord,r_twist,t_twist,sweep,operational_altitude,Re_numbers,Plot,csv_path)
        aero_df = pd.read_csv(input.aero_csv)
#2. Propeller Sizing   
 T_props, Position of Props, No.Props	M_props, M_engines
#3. Battery Sizing
    #3.1 Battery Consumption Model
        ##Prepare Inputs
        output_folder = input.output_folder
        V_vert_prop = input.V_stall*input.V_stall_safety_margin
        W = M_init*input.g
        D_rest = input.D_rest
        CLmax = max(aero_values_dic["CLs_corrected"])
        S_wing = S_mw
        aero_df = aero_df
        numberengines_vertical = input.numberengines_vertical
        numberengines_horizontal = input.numberengines_horizontal
        propeller_wake_efficiency = input.propeller_wake_efficiency
        number_relay_stations = number_relay_stations
        UAV_off_for_recharge_time_min = input.UAV_off_for_recharge_time_min
        battery_recharge_time_min = input.battery_recharge_time_min
        PL_power = input.PL_power
        show = input.show_plots
        ##Run
        max_battery_energy = Battery_Model(output_folder,aero_df,V_vert_prop,W,D_rest,CLmax,S_wing,numberengines_vertical,numberengines_horizontal,propeller_wake_efficiency,number_relay_stations,UAV_off_for_recharge_time_min,battery_recharge_time_min,PL_power,show)
    #3.2 Battery Sizing
        ##Prepare Inputs
        max_battery_energy = max_battery_energy
        battery_safety_margin = input.battery_safety_margin
    	battery_energy_density = input.battery_energy_density
        battery_volumetric_density = input.battery_volumetric_density
        ##Run
        battery_mass,battery_volume = Battery_Size(max_battery_energy,battery_safety_margin,battery_energy_density,battery_volumetric_density)


#4. Tail Sizing
#5. Structure Sizing
#6. Final Mass Calculation
        M_final = M_init + input.M_PL
