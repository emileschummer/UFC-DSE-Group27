import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from Battery_Modelling.Modelling.races import *
from Battery_Modelling.Sensitivity_Analysis.plot_power import *

if __name__ == "__main__":
    flat_race()
    get_race_results()    
    plot_race_results("Battery_Modelling/Output")
    plot_power_vs_velocity_sensitivity()
