import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from Modelling.races import *
from Sensitivity_Analysis.plot_power import *

def main():
    #flat_race() 
    #plot_race_results("Battery_Modelling/Output")
    #plot_power_vs_velocity_sensitivity()
    get_race_results("Battery_Modelling/Output",iterations=5)#50)   

if __name__ == "__main__":
    races.flat_race()  
    races.plot_race_results(output_folder="Battery_Modelling/Output")  
    plot_power.plot_power_vs_velocity_sensitivity(slope=0, iterations=100, variance=0.1) 
    plot_power.get_race_results(iterations=100, variance=0.1) 

