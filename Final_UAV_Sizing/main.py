#DSE Group 27 - UAV For Cycling
#import packages
import numpy as np
import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
import time
from scipy.optimize import curve_fit
import gc
#import functions
from Input import fixed_input_values as input
from Modelling.Wing_Sizing.Functions import wing_geometry_calculator
from Modelling.Wing_Sizing.AeroMain import run_full_aero
from Modelling.Wing_Sizing.AerodynamicForces import load_distribution_halfspan
from Modelling.Propeller_and_Battery_Sizing.Model.Battery_modelling import Battery_Model, Battery_Size
from Modelling.Tail_Sizing.Tail_sizing_final import get_tail_size
#Structures imports
from Modelling.Structural_Sizing.Main import Structure_Main
from Modelling.Structural_Sizing.Materials import Aluminum7075T6, Aluminum2024T4, NaturalFibre

def main_iteration(outputs,number_relay_stations, M_list,start_time):
    M_init = M_list[-1]  # Initial mass for the iteration
    i=0
    #0. Open General Files
    """Check OG_aero file is correct. It is never edited during iterations. only aero.csv is edited"""
    aero_df = pd.read_csv(input.OG_aero_csv)
    while abs(M_list[-1] - M_list[-2]) > input.min_delta_mass and abs(M_list[-1] - M_list[-2]) < input.max_delta_mass :
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
        M_prop =  3.75 #Final value for propeller mass

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
        tail_span = 1.55#from propellers
        Clhmax = input.Clhmax
        Cd0_wing = aero_df.loc[(aero_df["CL_corrected"] - 0).abs().idxmin(), "CD_vlm"]
        output_folder = outputs
        ##Run
        Sh, Clh0, tail_span_loop, tail_chord_loop,lh,max_tail_force = get_tail_size(W, piAe, Clalpha,Clhalpha,Cl0,S,Cmac,lh,l,Iy,c,plot,tail_span,Clhmax,Cd0_wing,output_folder)
#5. Structure Sizing
        print("\n--------------------------------------------------")
        print("Structure Sizing")

    #5.1 Prepare load distributions TODO

        cl_values_at_15 = np.array([0.06434802, 0.13850818, 0.21262615, 0.28667936, 0.36064524, 0.43450126,
        0.50822493, 0.58179379, 0.65518543, 0.7283775,  0.80134769, 0.87407379,
        0.94653363, 1.01870515, 1.09056636, 1.16209538, 1.23327041, 1.30406977,
        1.37447191, 1.44445536, 1.51399882, 1.5830811,  1.65168116, 1.7197781,
        1.78735118, 1.85437982, 1.92084359, 1.98672226, 1.99888533, 1.92394663,
        1.84900793, 1.77406923, 1.69913053, 1.62419183, 1.54925313, 1.47431442,
        1.39937572, 1.32443702, 1.24949832, 1.17455962, 1.09962092])

        # Assume these are at equally spaced spanwise stations from 0 to b/2
        n = len(cl_values_at_15)
        span = 3  # Example: total span = 3 m (adjust as needed)
        y = np.linspace(0, span/2, n)  # y = 0 at root, y = b/2 at tip

        # Fit cl_max to best match the data

        def elliptical(y, cl_max):
            return cl_max * np.sqrt(1 - (y/(span/2))**2)

        cl_max_fit, _ = curve_fit(elliptical, y, cl_values_at_15, p0=[2.0])

        # Now you can use this function as the elliptical approximation:
        def elliptical_cl(y):
            return cl_max_fit[0] * 1.225 * (100/3)**2 * np.sqrt(1 - (y/(span/2))**2)

        def elliptical_cd(y):
            return 0.125 * elliptical_cl(y)

        lift_distrib = elliptical_cl
        drag_distrib = elliptical_cd

    #5.2 Run Structure_Main

        Leg_Mass,Vtol_Pole_Mass,WingBox_Mass,Fuselage_Mass,Structure_mass,Total_Mass =  Structure_Main(
                Materials_Input=[Aluminum7075T6(), # VTOL Pole Material
                                Aluminum2024T4(), # Wing Box Material
                                Aluminum2024T4(), # Legs Material
                                NaturalFibre(),   # Fuselage Material
                                NaturalFibre()],  # Airfoil Material

               VTOL_Input=[0.01,        # VTOL Pole Inner Radius [m],
                           0.736,       # VTOL Prop Diameter [m],
                           InputWeight/4,        # VTOL Force [N],
                           2.6],       # VTOL Torque [Nm/m]

               Tail_Input=[tail_chord_loop,        # Tail Chord [m],
                           tail_span_loop,           #Tail Span [m],
                           0.2*Sh*(100/3)**2*1.225*1/2,          #Horizontal Distributed Load [N/m], # TODO
                           25],         #Vertical Distributed Load [N/m] # TODO

               Legs_Input=[0.30,        # Leg Length [m],
                           InputWeight/input.g],         #UAV Total mass [kg]

               Wing_Input=[3,         # Wing Box Length [m], TODO
                           0.65,        #MAC, TODO
                           18,          #Max Wing Torque [Nm],
                           lift_distrib,  #Lift Distribution [N/m], # TODO
                           drag_distrib],  #Drag Distribution [N/m] # TODO

               Fuselage_Input=[0.125,   #Fuselage Inner Radius [m],
                               0.1,     #Fuselage Section 1 Length [m], TODO
                               0.3,     #Fuselage Section 2 Length [m], TODO
                               0.4,     #Fuselage Section 3 Length [m], TODO
                               0.4,     #Payload Location [m], TODO
                               0.6,     #Wing Hole Location [m], TODO
                               140,      #Main Engine Thrust [N], TODO depends on total mass
                               3,      #Main Engine Torque [Nm/m],
                               1.85,       #Fuselage Section 1 Mass [kg],
                               M_battery,       #Fuselage Section 2 Mass [kg],
                               0.65,     #Filming equipment mass [kg],
                               10],     #Payload Drag [N] TODO

               SF=1.5,BigG=1.1) # Safety Factor, G load factor	

        M_struc = Structure_mass # Total Structure Mass
#6. Final Mass Calculation
        M_final = input.M_PL + M_prop +M_battery + M_struc
        M_list.append(M_final)
        print(f"Payload Mass: {input.M_PL} kg, Propeller Mass: {M_prop} kg, Battery Mass: {M_battery} kg, Structure Mass: {M_struc} kg")
        print(f"Final Mass for {number_relay_stations} Relay Stations: {M_final} kg (iteration {i})")
        runtime = time.time() - start_time
        hours, rem = divmod(runtime, 3600)
        minutes, seconds = divmod(rem, 60)
        print(f"Current Runtime of main: {int(hours):02d}:{int(minutes):02d}:{int(seconds):02d} (h:m:s)")
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
    output_dir = input.output_folder
    os.makedirs(output_dir, exist_ok=True)
    plt.savefig(os.path.join(output_dir, "mass_through_iterations.png"))
    if input.show_plots: plt.show()
    plt.close()
class Tee(object):
    def __init__(self, *files):
        self.files = files

    def write(self, obj):
        for f in self.files:
            f.write(obj)
            f.flush()

    def flush(self):
        for f in self.files:
            f.flush()
def main():
        # Only set up the Tee once, at the start of the main run
    if not hasattr(sys, "_stdout_tee_installed"):
        log_path = os.path.join(input.output_folder, "run_log.txt")
        os.makedirs(input.output_folder, exist_ok=True)
        sys.stdout = Tee(sys.__stdout__, open(log_path, "w"))
        sys._stdout_tee_installed = True
    M_dict = {}
    start_time = time.time()
    for number_relay_stations in range(input.min_RS,input.max_RS+1):
        M_list = [input.M_init+2*input.min_delta_mass]
        M_list.append(input.M_init)
        # Create output folder for this relay station
        outputs = os.path.join(input.output_folder, f"RS_{number_relay_stations}")
        os.makedirs(outputs, exist_ok=True)
        M_list = main_iteration(outputs,number_relay_stations, M_list, start_time)
        gc.collect()
        M_dict[number_relay_stations] = M_list
    print(M_dict)
    for number_relay_stations in M_dict.keys():
        print(f"Final mass for {number_relay_stations} Relay Stations: {M_dict[number_relay_stations][-1]} kg")
    plot_results(M_dict)
    end_time = time.time()
    runtime = end_time - start_time
    hours, rem = divmod(runtime, 3600)
    minutes, seconds = divmod(rem, 60)
    print(f"Total Runtime of main: {int(hours):02d}:{int(minutes):02d}:{int(seconds):02d} (h:m:s)")


if __name__ == "__main__":
    main()
