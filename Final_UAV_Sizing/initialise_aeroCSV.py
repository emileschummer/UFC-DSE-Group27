import os
from Modelling.Wing_Sizing.AeroMain import run_full_aero
from Modelling.Wing_Sizing.Functions import no_quarterchord_sweep
from Input import fixed_input_values as input

airfoil_dat_path = os.path.join("Final_UAV_Sizing", "Input", "AirfoilData", "Airfoil.dat")
name = "S1223"
xfoil_path = input.xfoil
operational_velocity = input.V_stall*input.V_stall_safety_margin
num_spanwise_sections = input.num_spanwise_sections
vlm_chordwise_resolution = input.vlm_chordwise_resolution
delta_alpha_3D_correction = input.delta_alpha_3D_correction
alpha_range2D= input.alpha_range2D
alpha_range3D = input.alpha_range3D
S=1
r_chord = 4*S/(input.b*(1 + input.taper_ratio))
t_chord = r_chord*input.taper_ratio
r_twist = input.r_twist
t_twist = input.t_twist
sweep = no_quarterchord_sweep(r_chord,t_chord) # [deg] quarter-chord sweep angle
operational_altitude = input.altitude
Re_numbers = input.Re_numbers
Plot = input.show_plots
csv_path = input.aero_csv
output_folder = "Final_UAV_Sizing/Output"
##Run
"""aero_values_dic={
"wing_geom": wing_geom,
"airplane_geom": airplane_geom,
"CDs_vlm_original": CDs_vlm_original,
"CLs_corrected": CLs_corrected,
"lift_distribution": lift_distribution,
"alphas" : alpha_range3D"""
aero_values_dic = run_full_aero(num_spanwise_sections=num_spanwise_sections,airfoil_dat_path = airfoil_dat_path, name = name, xfoil_path=xfoil_path,operational_velocity=operational_velocity,vlm_chordwise_resolution = vlm_chordwise_resolution,delta_alpha_3D_correction = delta_alpha_3D_correction,alpha_range2D = alpha_range2D,alpha_range3D = alpha_range3D,operational_altitude = operational_altitude,Re_numbers = Re_numbers,Plot = Plot,csv_path = csv_path, r_chord = r_chord,t_chord = t_chord,r_twist = r_twist,t_twist = t_twist,sweep = sweep,output_folder=output_folder)
