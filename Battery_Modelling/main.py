import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from Battery_Modelling.Modelling.races import *

def main():
    flat_race()
    get_race_results("Battery_Modelling/Output")
    plot_power_vs_velocity()

if __name__ == "__main__":
    main()