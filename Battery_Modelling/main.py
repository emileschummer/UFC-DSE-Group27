from Modelling.races import *

from Modelling.races import *
from Sensitivity_Analysis.plot_power import *

def main():
    #flat_race() 
    #plot_race_results("Battery_Modelling/Output")
    plot_power_vs_velocity_sensitivity()
    get_race_results(iterations=10)   
if __name__ == "__main__":
    flat_race()
    get_race_results("Battery_Modelling/Output")
    plot_power_vs_velocity()

if __name__ == "__main__":
    main()
