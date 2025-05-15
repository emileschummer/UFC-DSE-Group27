import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from Modelling.races import *
from Sensitivity_Analysis.plot_power import *

def main(output_folder="Battery_Modelling/Output_test"):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)  # Create the output folder if it doesn't exist
    #flat_race(output_folder) 
    #plot_race_results(output_folder, show = False)
    plot_power_vs_velocity_sensitivity(output_folder,slope=0, iterations = 100, variance = 0.1, show = True)
    #get_race_results(output_folder, iterations=50, variance=0.1) 

if __name__ == "__main__":
    main("Battery_Modelling/Output")#_TradeOff_50iterations_0.1variance")
