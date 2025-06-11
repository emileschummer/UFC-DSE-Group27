import numpy as np
#Fixed input values for UAV sizing
##A. Folder paths
output_folder = "Final_UAV_Sizing/Output" # [str] folder to save output data
aero_csv = "Final_UAV_Sizing/Input/WingData/aero.csv" # [str] name of the CSV file to save aerodynamic data
##B. Constants
g = 9.81 # [m/s2] gravity acceleration
##C. Speed
V_stall = 10 # [m/s] actual stall speed of wing
V_stall_safety_margin = 1.1 # [-] safety margin for stall speed

##0. Iteration parameters
show_plots = False
M_init = 15 # [kg] initial mass of UAV for iteration
delta_mass = 0.01 # [kg], mass convergence
max_RS = 6 # [-] maximum number of relay stations

##1. Wing Sizing Parameters
xfoil = "Xfoil" # [str] path to xfoil executable
altitude =  # [m] operational altitude for wing sizing
taper_ratio =  # [-] taper ratio for wing sizing
b = 3 # [m] wing span
num_spanwise_sections = 200 # [-] number of spanwise sections for VLM analysis
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
propeller_wake_efficiency = 0.8

##3. Battery Sizing
output_folder = "Final_UAV_Sizing/Output/Battery" # [str] folder to save battery data
D_rest =  # [N] Drag of the rest
UAV_off_for_recharge_time_min = 15 # [min] time UAV is not filming to recharge
battery_recharge_time_min = 5 # [min] time to change/recharge battery
PL_power = 189 # [W] power consumption of payload
battery_safety_margin = #1.2 # [-] safety margin for battery capacity
battery_energy_density = 450 # [Wh/kg] energy density of battery
battery_volumetric_density =  # [Wh/m^3] volumetric density of battery
##4. Tail Sizing
##5. Structure Sizing
##6. Final Mass Calculation
M_PL =  # [kg] mass of payload