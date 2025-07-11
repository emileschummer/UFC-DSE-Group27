import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from datetime import datetime

from Modelling.races import *
from Midterm_Battery_Modelling.Modelling.plot_power import *
from Input import Configuration_inputs as config

def main(output_folder="Battery_Modelling/Output"):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)  # Create the output folder if it doesn't exist
    #flat_race(output_folder) 
    plot_race_results(output_folder, show = True)
    #plot_power_vs_velocity_sensitivity(output_folder,slope=0, iterations = 1, variance = 0, show = True)
    #get_race_results(output_folder,battery_capacity=2812.5, iterations=1, variance=0) 
    #Battery Density: 450Wh/kg, ratio MTOW: 0.25

if __name__ == "__main__":
    W = config.inputs_list_original[0][0]
    CLmax = (config.inputs_list_original[2][5] +config.inputs_list_original[3][5])/2
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_folder = f"Battery_Modelling/Output/{timestamp}_W{W}_CLmax{CLmax}"
    main(output_folder)
