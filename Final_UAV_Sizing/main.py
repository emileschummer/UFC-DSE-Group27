#DSE Group 27 - UAV For Cycling
#import packages
import numpy as np
import os
import pandas as pd
#import functions
import Final_UAV_Sizing.Input.fixed_input_values as input
from Final_UAV_Sizing.Modelling.Wing_Sizing.Functions import wing_geometry_calculator
from Final_UAV_Sizing.Modelling.Wing_Sizing.AeroMain import run_full_aero
from Final_UAV_Sizing.Modelling.Wing_Sizing.AerodynamicForces import load_distribution_halfspan
from Final_UAV_Sizing.Modelling.Propeller_and_Battery_Sizing.Model.Battery_modelling import Battery_Model, Battery_Size
from Final_UAV_Sizing.Modelling.Tail_Sizing.Tail_sizing_final import get_tail_size




for number_relay_stations in range(1,input.max_RS):
    M_init = input.M_init
    M_final = 0
    #0. Open General Files
    aero_df = pd.read_csv(input.OG_aero_csv)
    while abs(M_init - M_final) > input.delta_mass:
        M_init = M_final
#1. Wing Sizing
    #1.1 Wing Geometry
        ##Prepare input values
        InputWeight = M_init * input.g
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
    #1.3 Load Distribution
        ##Prepare input values
        wing_geom = aero_values_dic["wing_geom"]
        lift_distribution = aero_values_dic["lift_distribution"]
        alpha = aero_values_dic["alphas"][np.argmax(aero_values_dic["CLs_corrected"])]
        half_span = input.b/2
        plot = input.show_plots
        ##Run
        load_distribution_halfspan(wing_geom,lift_distribution,alpha,half_span,plot)
#2. Propeller Sizing   
        """From Prop, we need whatever values Jadon needs, such as
 T_props, Position of Props, No.Props	M_props, M_engines, CD0_total
 
 We also need CD0 and tail_span for Tijn's Tail Sizing. As well as the propeller mass estimated below roughly (pls change)"""
        M_prop = 2 #Placeholder for propeller mass
#3. Battery Sizing
    #3.1 Battery Consumption Model
        ##Prepare Inputs
        output_folder = input.output_folder
        V_vert_prop = input.V_stall*input.V_stall_safety_margin
        W = M_init*input.g
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
        max_battery_energy = Battery_Model(output_folder,aero_df,V_vert_prop,W,CLmax,S_wing,numberengines_vertical,numberengines_horizontal,propeller_wake_efficiency,number_relay_stations,UAV_off_for_recharge_time_min,battery_recharge_time_min,PL_power,show)
    #3.2 Battery Sizing
        ##Prepare Inputs
        max_battery_energy = max_battery_energy
        battery_safety_margin = input.battery_safety_margin
        battery_energy_density = input.battery_energy_density
        battery_volumetric_density = input.battery_volumetric_density
        ##Run
        M_battery,battery_volume = Battery_Size(max_battery_energy,battery_safety_margin,battery_energy_density,battery_volumetric_density)


#4. Tail Sizing
    #4.1 Horizontal Tail
        ##Prepare Inputs
        W = M_init*input.g
        piAe = np.pi * input.b**2 / S_mw * input.e
        Clalpha = np.polyfit(aero_df["alphas"][:aero_df["CLs_corrected"].idxmax()+1], aero_df["CLs_corrected"][:aero_df["CLs_corrected"].idxmax()+1], 1)[0]
        Clhalpha = input.Clhalpha
        Cl0 = aero_df.loc[(aero_df["alphas"] - 0).abs().idxmin(), "CLs_corrected"]
        S = S_mw
        Cd0 = input.Cd0 #from propellers
        Cmac = aero_df.loc[(aero_df["CLs_corrected"] - 0).abs().idxmin(), "Cm_vlm"]
        lh = input.lh
        l = input.l
        Iy = input.Iy
        c = S_mw/input.b
        plot = input.show_plots
        """adjust tail_span to necessary value"""
        tail_span = 1#from propellers
        Clhmax = input.Clhmax
        ##Run
        Sh, Clh0, span, cord,lh,max_tail_force = get_tail_size(W, piAe, Clalpha, Clhalpha,Cl0,S,Cd0,Cmac,lh,l,Iy,c,plot,tail_span,Clhmax)
#5. Structure Sizing
        M_struc = 5
#6. Final Mass Calculation
        M_final = input.M_PL + M_prop +M_battery + M_struc
