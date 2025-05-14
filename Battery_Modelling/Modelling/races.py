import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import numpy as np
from matplotlib import pyplot as plt

from Battery_Modelling.Modelling.UFC_MMA_1_Helicopter import calculate_power_UFC_MMA_1
from Battery_Modelling.Modelling.UFC_MMA_2_Quad import calculate_power_UFC_MMA_2
from Battery_Modelling.Modelling.UFC_MMA_3_Osprey import calculate_power_UFC_MMA_3
from Battery_Modelling.Modelling.UFC_MMA_4_Yangda import calculate_power_UFC_MMA_4
from Battery_Modelling.Input import Strava_input_csv as sva
from Battery_Modelling.Input.Configuration_inputs import *

def plot_race_results(output_folder="Output"):
    races = sva.make_race_dictionnary()
    race_results = {}
    for race_name, race_data in races.items():
        fig, axs = plt.subplots(3, 1, figsize=(12, 10), sharex=True)  # Create subplots
        race_configurations_plot = []
        for i in range(4):
            race_plot = []
            if i == 0:
                calculate_power = calculate_power_UFC_MMA_1
                label = 'Helicopter'
                inputs = [W,eta,CD_MMA1,S_MMA1,A_MMA1]
            elif i == 1:
                calculate_power = calculate_power_UFC_MMA_2
                label = 'Quadcopter'
                inputs = [W, eta, CD_MMA2, Stop_MMA2, Sfront_MMA2, totalA_MMA2, numberengine_MMA2]
            elif i == 2:
                calculate_power = calculate_power_UFC_MMA_3
                label = 'Osprey'
                inputs = [W, eta, CD0_MMA3, piAe_MMA3, S_MMA3, CLmax_MMA3, r_MMA3, numberengines_MMA3]
            elif i == 3:
                calculate_power = calculate_power_UFC_MMA_4
                label = 'Yangda'
                inputs = [W, eta, CD0_MMA4, piAe_MMA4, S_MMA4, CLmax_MMA4, r_MMA4, prop_efficiency_MMA4, numberengines_vertical_MMA4, numberengines_horizontal_MMA4]
                high_speed_energy_count = 0
            energy = 0
            t = 0
            time_plot = []
            power_plot = []
            speed_plot = []
            gradient_plot = []
            for index, row in race_data.iterrows():
                time = row[" time"]  # Access directly from DataFrame row
                velocity_smooth = row[" velocity_smooth"]
                grade_smooth = np.arctan(row[" grade_smooth"] / 100)
                altitude = row[" altitude"]
                rho = sva.air_density_isa(altitude)
                P = calculate_power(grade_smooth, velocity_smooth, rho, inputs)
                time_diff = time - t
                energy = energy + time_diff * P
                t = time
                time_plot.append(time)
                power_plot.append(P)
                speed_plot.append(velocity_smooth)
                gradient_plot.append(row[" grade_smooth"])
                if i == 3: #Analysing yangda
                    if velocity_smooth > 15:
                        high_speed_energy_count += P * time_diff
            race_plot.append([time_plot, power_plot])
            if race_name not in race_results:
                race_results[race_name] = [0] * 4
            race_results[race_name][i] = energy / 3600  # Store energy in Wh
            axs[0].plot(time_plot, power_plot, label=label)  # Plot power vs time in the first subplot

        # Highlight regions where speed > 15 m/s
        speed_count = 0
        for j in range(len(speed_plot) - 1):
            if speed_plot[j] > 15:
                axs[0].axvspan(time_plot[j], time_plot[j + 1], color='blue', alpha=0.2)
                speed_count+=1
        print(f"---------{race_name} Speed Profile---------")
        print(f"Maximum speed: {max(speed_plot)} m/s")
        print(f"Speed < 15 m/s (stall): {1-speed_count/len(speed_plot)} of time")
        print("---------UFC-MMA-4 Yangda---------")
        print(f"Relative Power use of Yangda when speed < 15 m/s: {1-high_speed_energy_count/race_results[race_name][3]/3600}")
        axs[1].plot(time_plot, speed_plot, label='Speed', color='black')  # Plot speed vs time
        axs[2].plot(time_plot, gradient_plot, label='Gradient', color='grey')  # Plot gradient vs time

        # Set titles and labels for subplots
        axs[0].set_title(f"Power vs Time for {race_name}")
        axs[0].set_ylabel("Power (W)")
        axs[0].legend()
        axs[0].grid()

        axs[1].set_title("Speed vs Time")
        axs[1].set_ylabel("Speed (m/s)")
        axs[1].legend()
        axs[1].grid()

        axs[2].set_title("Gradient vs Time")
        axs[2].set_xlabel("Time (s)")
        axs[2].set_ylabel("Gradient (%)")
        axs[2].legend()
        axs[2].grid()

        # Save the figure
        os.makedirs(output_folder, exist_ok=True)  # Ensure the output folder exists
        output_path = os.path.join(output_folder, f"{race_name}_power_speed_gradient_vs_time.png")
        plt.tight_layout()
        plt.savefig(output_path)
        plt.show()
    print(race_results)


def flat_race():
    print("---------7h Flat Race at 50km/h---------")
    print("UFC-MMA-1 Helicopter Energy (Wh): ",calculate_power_UFC_MMA_1(0,50/3.6,1.225)*7)
    print("UFC-MMA-2 Quadcopter Energy (Wh): ",calculate_power_UFC_MMA_2(0,50/3.6,1.225)*7)
    print("UFC-MMA-3 Osprey Energy (Wh): ",calculate_power_UFC_MMA_3(0,50/3.6,1.225)*7)
    print("UFC-MMA-4 Yangda Energy (wh): ",calculate_power_UFC_MMA_4(0,50/3.6,1.225)*7)