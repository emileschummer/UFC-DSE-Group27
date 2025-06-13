import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from datetime import datetime

from Model.races import *
from Model.Battery_modelling import Battery_Model
from Input.Config import *


def main(output_folder="Battery_Modelling/Output"):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)  # Create the output folder if it doesn't exist
    #flat_race(output_folder) 
    #plot_race_results(output_folder, show = False)
    print(Battery_Model(output_folder, show=True))

if __name__ == "__main__":
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_folder = f"battery_test"
    main(output_folder)
