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
<<<<<<< HEAD
    main()
=======
    # Example usage
    plot_power_vs_velocity_sensitivity(slope=0, iterations=10, variance=0.1)

>>>>>>> 3088b7379d6a57232919417950465ad3038d8133
