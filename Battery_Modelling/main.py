import Modelling.races as races
import Sensitivity_Analysis.plot_power as plot_power


if __name__ == "__main__":
    races.flat_race()  
    races.plot_race_results(output_folder="Battery_Modelling/Output")  
    plot_power.plot_power_vs_velocity_sensitivity(slope=0, iterations=100, variance=0.1) 
    plot_power.get_race_results(iterations=100, variance=0.1) 

