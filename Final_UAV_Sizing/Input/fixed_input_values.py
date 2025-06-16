import numpy as np
from datetime import datetime
#Fixed input values for UAV sizing
##A. Folder paths
timestamp = datetime.now().strftime("%m-%d_%H-%M")
output_folder = f"Final_UAV_Sizing/Output/Run_on_{timestamp}" # [str] folder to save output data
OG_aero_csv = "Final_UAV_Sizing/Input/WingData/OG_aero.csv" # [str] name of the original CSV file to save aerodynamic data
aero_csv = "Final_UAV_Sizing/Input/WingData/aero.csv" # [str] name of the CSV file to save aerodynamic data
##B. Constants
g = 9.81 # [m/s2] gravity acceleration
##C. Speed
V_stall = 10 # [m/s] actual stall speed of wing
V_stall_safety_margin = 1.1 # [-] safety margin for stall speed

##0. Iteration parameters
show_plots = False
M_init = 15 # [kg] initial mass of UAV for iteration
min_delta_mass = 0.1 # [kg], mass convergence
max_delta_mass = 10 # [kg], mass explodes
min_RS = 3 # [-] minimum number of relay stations
max_RS = 6 # [-] maximum number of relay stations

##1. Wing Sizing Parameters
xfoil = r"Final_UAV_Sizing\XFOIL6.99\xfoil.exe"#"Final_UAV_Sizing/Xfoil" # [str] path to xfoil executable
"""Find adequate values for below"""
altitude =  0 # [m] operational altitude for wing sizing
taper_ratio = 0.4 # [-] taper ratio for wing sizing
"""Stop here"""
b = 3 # [m] wing span
num_spanwise_sections = int(200) # [-] number of spanwise sections for VLM analysis
vlm_chordwise_resolution = 6 # [-] chordwise resolution for VLM analysis
delta_alpha_3D_correction = 1.0 # [deg] correction for 3D stall angle
alpha_range2D= np.linspace(-10, 25, 36) # [deg] angle of attack range for 2D stall database
alpha_range3D = np.linspace(-10, 30, 41) # [deg] angle of attack range for 3D VLM analysis
r_twist = 0.0 # [deg] root twist angle
t_twist = 0.0 # [deg] tip twist angle
sweep = 0.0 # [deg] wing sweep angle
Re_numbers = 8 # [-] number of Reynolds numbers for stall database

##2. Propeller Sizing
numberengines_vertical = 4
numberengines_horizontal = 1
propeller_wake_efficiency = 0.7
S_wing = 2
CLmax = 2
V_vert_prop = V_stall * V_stall_safety_margin
L_blade = 0.7366
w_blade = 0.075
L_stab= 0.6
w_stab= 0.5
L_poles= 3.6*L_blade/2 + 0.5
w_poles= 0.34
L_motor = 0.3
L_gimbal = 0.12
L_speaker = 0.1
L_n = 0.2
L_c = 0.6
L_fus = 2*L_n + L_c
w_fus = S_wing / L_fus
d_fus = 0.25

##3. Battery Sizing
engine_input_folder = "Final_UAV_Sizing/Input/Prop_Engine_Data" 
UAV_off_for_recharge_time_min = 15 # [min] time UAV is not filming to recharge
battery_recharge_time_min = 5 # [min] time to change/recharge battery
PL_power = 155 # [W] power consumption of payload
"""Find propper value for safety_margin (including reserve)"""
battery_safety_margin = 1.2 # [-] safety margin for battery capacity
battery_energy_density = 450 # [Wh/kg] energy density of battery
battery_volumetric_density =  1851.9 # [kg/m^3] volumetric density of battery
"""Explain where these values come from and if linked to iteration (Roan knows)"""
"""until here"""
##4. Tail Sizing
e = 0.8 # [-] Oswald Efficiency
Clhalpha = 4.3 # [-] Clalpha of the tail
lh = 1 # [m] tail length from CG
l = 0 # [m] distance between CG and AC
Iy = 14 # [kgm^2] Mass Moment of Inertia
Clhmax = 1.5 # [-] Clmax of tail
##5. Structure Sizing
##6. Final Mass Calculation
M_PL = 2.063 # [kg] mass of payload