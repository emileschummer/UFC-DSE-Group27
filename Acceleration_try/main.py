import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from datetime import datetime

from Model.races import *
from Model.Battery_modelling import Battery_Model
from Input.Config import *
V_stall, W,D_rest,D_wing,L_wing,CLmax,alpha_T, N_blades, Chord_blade,CD_blade, omega, r_prop_vertical, numberengines_vertical, numberengines_horizontal, eta_prop_horizontal,eta_prop_vertical, propeller_wake_efficiency,number_relay_stations,battery_max_usage,VCr=8, 250,50,100,250,2,0, 2, 0.05,0.03,300, 0.2, 4,2,0.8,0.8,0.8,0.8,0.8,20
def main(output_folder="Battery_Modelling/Output"):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)  # Create the output folder if it doesn't exist
    #flat_race(output_folder) 
    #plot_race_results(output_folder, show = False)
    print(Battery_Model(V_stall, W,D_rest,D_wing,L_wing,CLmax,alpha_T, N_blades, Chord_blade,CD_blade, omega, r_prop_vertical, numberengines_vertical, numberengines_horizontal, eta_prop_horizontal,eta_prop_vertical, propeller_wake_efficiency,number_relay_stations,battery_max_usage,VCr,output_folder, show=True))

if __name__ == "__main__":
    W = input_list_final[0]
    CLmax = input_list_final[5]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_folder = f"test"
    main(output_folder)
