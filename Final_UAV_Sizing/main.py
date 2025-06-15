#DSE Group 27 - UAV For Cycling
#import packages
import numpy as np
import os
import pandas as pd
import matplotlib.pyplot as plt
#import functions
from Input import fixed_input_values as input
from Modelling.Wing_Sizing.Functions import wing_geometry_calculator
from Modelling.Wing_Sizing.AeroMain import run_full_aero
from Modelling.Wing_Sizing.AerodynamicForces import load_distribution_halfspan
from Modelling.Propeller_and_Battery_Sizing.Model.Battery_modelling import Battery_Model, Battery_Size
from Modelling.Tail_Sizing.Tail_sizing_final import get_tail_size

def main_iteration(outputs,number_relay_stations, M_list):
    M_init = M_list[-1]  # Initial mass for the iteration
    i=0
    #0. Open General Files
    """Check OG_aero file is correct. It is never edited during iterations. only aero.csv is edited"""
    aero_df = pd.read_csv(input.OG_aero_csv)
    while abs(M_list[-1] - M_list[-2]) > input.delta_mass:
        print("------------------------------------------------------------------------------------------------------------------------------------------------------")
        print("------------------------------------------------------------------------------------------------------------------------------------------------------")
        print(f"Iteration {i+1} for {number_relay_stations} Relay Stations with M_init ")
        print("------------------------------------------------------------------------------------------------------------------------------------------------------")
        i+=1
#1. Wing Sizing
        print("------------------------------------------------------------------------------------------------------------------------------------------------------")
        print("Wing Sizing")
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
        num_spanwise_sections = input.num_spanwise_sections
        vlm_chordwise_resolution = input.vlm_chordwise_resolution
        delta_alpha_3D_correction = input.delta_alpha_3D_correction
        alpha_range2D= input.alpha_range2D
        alpha_range3D = input.alpha_range3D
        r_chord = cr
        t_chord = ct
        r_twist = input.r_twist
        t_twist = input.t_twist
        sweep = input.sweep
        operational_altitude = input.altitude
        Re_numbers = input.Re_numbers
        Plot = input.show_plots
        csv_path = input.aero_csv
        output_folder = outputs
        ##Run
        """aero_values_dic={
        "wing_geom": wing_geom,
        "airplane_geom": airplane_geom,
        "CDs_vlm_original": CDs_vlm_original,
        "CLs_corrected": CLs_corrected,
        "lift_distribution": lift_distribution,
        "alphas" : alpha_range3D"""
        aero_values_dic = run_full_aero(num_spanwise_sections=num_spanwise_sections,airfoil_dat_path = airfoil_dat_path, name = name, xfoil_path=xfoil_path,operational_velocity=operational_velocity,vlm_chordwise_resolution = vlm_chordwise_resolution,delta_alpha_3D_correction = delta_alpha_3D_correction,alpha_range2D = alpha_range2D,alpha_range3D = alpha_range3D,operational_altitude = operational_altitude,Re_numbers = Re_numbers,Plot = Plot,csv_path = csv_path, r_chord = r_chord,t_chord = t_chord,r_twist = r_twist,t_twist = t_twist,sweep = sweep,output_folder = output_folder)
        aero_df = pd.read_csv(input.aero_csv)
    #1.3 Load Distribution
        ##Prepare input values
        wing_geom = aero_values_dic["wing_geom"]
        lift_distribution = aero_values_dic["lift_distribution"]
        alpha = aero_values_dic["alphas"][np.argmax(aero_values_dic["CLs_corrected"])]
        half_span = input.b/2
        plot = input.show_plots
        output_folder = outputs
        ##Run
        lift_distribution = load_distribution_halfspan(wing_geom,lift_distribution,alpha,half_span,plot,output_folder)
#2. Propeller Sizing 
        print("--------------------------------------------------")
        print("Propeller Sizing")  
        """From Prop, we need whatever values Jadon needs, such as
T_props, Position of Props, No.Props	M_props, M_engines, CD0_total

We also need CD0 and tail_span for Tijn's Tail Sizing. As well as the propeller mass estimated below roughly (pls change)"""
        M_prop = 2 #Placeholder for propeller mass

#3. Battery Sizing
        print("--------------------------------------------------")
        print("Battery Sizing")
    #3.1 Battery Consumption Model
        ##Prepare Inputs
        input_folder = input.engine_input_folder
        output_folder = outputs
        aero_df = aero_df
        data_folder="Final_UAV_Sizing/Input/RaceData"
        V_vert_prop = input.V_stall*input.V_stall_safety_margin
        W = M_init*input.g
        CLmax = aero_df["CL_corrected"].max()
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
        show_all = False #Set to True to show all race plots
        L_n = input.L_n
        L_c = input.L_c
        L_fus = L_n+L_c
        L_blade = input.L_blade
        L_stab = input.L_stab
        d_fus = input.d_fus
        w_fus = S_mw / input.L_fus
        w_blade = input.w_blade
        w_stab = input.w_stab
        L_poles = input.L_poles
        w_poles = input.w_poles
        L_motor =  input.L_motor
        L_gimbal =  input.L_gimbal
        L_speaker = input.L_speaker
        ##Run
        max_battery_energy = Battery_Model(input_folder,output_folder,aero_df,data_folder,V_vert_prop,W,CLmax,S_wing,numberengines_vertical,numberengines_horizontal,propeller_wake_efficiency,number_relay_stations,UAV_off_for_recharge_time_min,battery_recharge_time_min,PL_power,show,show_all,L_fus,L_n,L_c,L_blade,L_stab, d_fus, w_fus, w_blade, w_stab, L_poles, w_poles, L_motor, L_gimbal, L_speaker)
    #3.2 Battery Sizing
        ##Prepare Inputs
        max_battery_energy = max_battery_energy
        battery_safety_margin = input.battery_safety_margin
        battery_energy_density = input.battery_energy_density
        battery_volumetric_density = input.battery_volumetric_density
        ##Run
        M_battery,battery_volume = Battery_Size(max_battery_energy,battery_safety_margin,battery_energy_density,battery_volumetric_density)

#4. Tail Sizing
        print("--------------------------------------------------")
        print("Tail Sizing")
    #4.1 Horizontal Tail
        ##Find Clalpha
        cl_corr = aero_df["CL_corrected"]
        alpha_deg = aero_df["alpha (deg)"]
        start_idx = alpha_deg[alpha_deg >= 0].index[0]
        clmax_idx = cl_corr[start_idx:].idxmax()
        cl_corr_inc = cl_corr.loc[start_idx:clmax_idx]
        alpha_inc_deg = alpha_deg.loc[start_idx:clmax_idx]
        alpha_inc_rad = np.deg2rad(alpha_inc_deg)
        coeffs = np.polyfit(alpha_inc_rad, cl_corr_inc, 1)
        Clalpha = coeffs[0]
        ##Prepare Inputs
        W = M_init*input.g
        piAe = np.pi * input.b**2 / S_mw * input.e
        Clalpha=Clalpha
        Clhalpha = input.Clhalpha
        Cl0 = aero_df.loc[(aero_df["alpha (deg)"] - 0).abs().idxmin(), "CL_corrected"]
        S = S_mw
        """Cmac is posing problems. a value of -0.5 is expected by Tijn, but roughly 0 is obtained"""
        Cmac = aero_df.loc[(aero_df["CL_corrected"] - 0).abs().idxmin(), "Cm_vlm"]
        lh = input.lh
        l = input.l
        Iy = input.Iy
        c = S_mw/input.b
        plot = input.show_plots
        """adjust tail_span to necessary value from structure or propellers idk"""
        tail_span = 1#from propellers
        Clhmax = input.Clhmax
        Cd0_wing = aero_df.loc[(aero_df["CL_corrected"] - 0).abs().idxmin(), "CD_vlm"]
        output_folder = outputs
        ##Run
        Sh, Clh0, span, cord,lh,max_tail_force = get_tail_size(W, piAe, Clalpha,Clhalpha,Cl0,S,Cmac,lh,l,Iy,c,plot,tail_span,Clhmax,Cd0_wing,output_folder)
#5. Structure Sizing
        print("\n--------------------------------------------------")
        print("Structure Sizing")
        M_struc = 5
#6. Final Mass Calculation
        M_final = input.M_PL + M_prop +M_battery + M_struc
        M_list.append(M_final)
        print(f"Final Mass for {number_relay_stations} Relay Stations: {M_final} kg (iteration {i})")
    return M_list
def plot_results(M_dict):
    fig, axs = plt.subplots(1, 4, figsize=(20, 5), sharey=True)
    relay_station_counts = list(M_dict.keys())

    for idx, number_relay_stations in enumerate(relay_station_counts[:4]):
        axs[idx].plot(M_dict[number_relay_stations], marker='o')
        axs[idx].set_title(f"{number_relay_stations} Relay Stations")
        axs[idx].set_xlabel("Iteration")
        axs[idx].set_ylabel("Mass (kg)")
        axs[idx].grid(True)

    plt.tight_layout()
    plt.show()
def main(plot = False):
    M_dict = {}
    for number_relay_stations in range(input.min_RS,input.max_RS):
        M_list = [0]
        M_list.append(input.M_init)
        # Create output folder for this relay station
        outputs = os.path.join(input.output_folder, f"RS_{number_relay_stations}")
        os.makedirs(outputs, exist_ok=True)
        M_list = main_iteration(outputs,number_relay_stations, M_list)
        M_dict[number_relay_stations] = M_list
    for number_relay_stations in range(M_dict.keys()):
        print(f"Final mass for {number_relay_stations} Relay Stations: {M_dict[number_relay_stations][-1]} kg")
    if plot:
        plot_results(M_dict)


if __name__ == "__main__":
    main(plot=True)




"""#3. Battery Sizing
print("--------------------------------------------------")
print("Battery Sizing")
#3.1 Battery Consumption Model
##Prepare Inputs
input_folder = input.engine_input_folder
output_folder = input.output_folder
aero_df = pd.read_csv(input.OG_aero_csv)
data_folder="Final_UAV_Sizing/Input/RaceData"
V_vert_prop = input.V_stall*input.V_stall_safety_margin
W = input.M_init*input.g
CLmax = aero_df["CL_corrected"].max()
S_wing = 2#S_mw
aero_df = aero_df
numberengines_vertical = input.numberengines_vertical
numberengines_horizontal = input.numberengines_horizontal
propeller_wake_efficiency = input.propeller_wake_efficiency
number_relay_stations = 3
UAV_off_for_recharge_time_min = input.UAV_off_for_recharge_time_min
battery_recharge_time_min = input.battery_recharge_time_min
PL_power = input.PL_power
show = input.show_plots
L_n = input.L_n
L_c = input.L_c
L_fus = L_n+L_c
d = input.d
L_blade = input.L_blade
L_stab = input.L_stab
##Run
max_battery_energy = Battery_Model(input_folder,output_folder,aero_df,data_folder,V_vert_prop,W,CLmax,S_wing,numberengines_vertical,numberengines_horizontal,propeller_wake_efficiency,number_relay_stations,UAV_off_for_recharge_time_min,battery_recharge_time_min,PL_power,show,L_fus,L_n,L_c,d,L_blade,L_stab)
#3.2 Battery Sizing
##Prepare Inputs
max_battery_energy = max_battery_energy
battery_safety_margin = input.battery_safety_margin
battery_energy_density = input.battery_energy_density
battery_volumetric_density = input.battery_volumetric_density
##Run
M_battery,battery_volume = Battery_Size(max_battery_energy,battery_safety_margin,battery_energy_density,battery_volumetric_density)
print(M_battery,battery_volume)"""