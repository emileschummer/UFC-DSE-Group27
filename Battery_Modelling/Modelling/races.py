import numpy as np
from matplotlib import pyplot as plt

from Modelling.UFC_MMA_1_Helicopter import calculate_power_UFC_MMA_1
from Modelling.UFC_MMA_2_Quad import calculate_power_UFC_MMA_2
from Modelling.UFC_MMA_3_Osprey import calculate_power_UFC_MMA_3
from Modelling.UFC_MMA_4_Yangda import calculate_power_UFC_MMA_4
from Input import Strava_input_csv as sva
import os

def get_race_results(output_folder="Output"):
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
            elif i == 1:
                calculate_power = calculate_power_UFC_MMA_2
                label = 'Quadcopter'
            elif i == 2:
                calculate_power = calculate_power_UFC_MMA_3
                label = 'Osprey'
            elif i == 3:
                calculate_power = calculate_power_UFC_MMA_4
                label = 'Yangda'
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
                P = calculate_power(grade_smooth, velocity_smooth, rho)
                time_diff = time - t
                energy = energy + time_diff * P
                t = time
                time_plot.append(time)
                power_plot.append(P)
                speed_plot.append(velocity_smooth)
                gradient_plot.append(row[" grade_smooth"])
            race_plot.append([time_plot, power_plot])
            if race_name not in race_results:
                race_results[race_name] = [0] * 4
            race_results[race_name][i] = energy / 3600  # Store energy in Wh
            axs[0].plot(time_plot, power_plot, label=label)  # Plot power vs time in the first subplot
        axs[1].plot(time_plot, speed_plot, label='Speed', color='black', linestyle='--')  # Plot speed vs time
        axs[2].plot(time_plot, gradient_plot, label='Gradient', color='grey', linestyle='--')  # Plot gradient vs time

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

def plot_power_vs_velocity():
    velocity = np.linspace(0,40,1000)
    slope = 20
    slope = slope*np.pi/180
    T = [[],[],[],[]]
    for v in velocity:
        T1 = calculate_power_UFC_MMA_1(slope,v,1.225)
        T2 = calculate_power_UFC_MMA_2(slope,v,1.225)
        T3 = calculate_power_UFC_MMA_3(slope,v,1.225)
        T4 = calculate_power_UFC_MMA_4(slope,v,1.225)
        T[0].append(T1)
        T[1].append(T2)
        T[2].append(T3)
        T[3].append(T4)
    import matplotlib.pyplot as plt

    plt.plot(velocity,T[0],label = 'Helicopter')
    plt.plot(velocity,T[1], label = 'Quadcopter')
    plt.plot(velocity,T[2], label = 'Osprey')
    plt.plot(velocity,T[3], label = 'Yangda')
    plt.legend()
    plt.show()

def flat_race():
    print("UFC-MMA-1 Helicopter Energy (Wh): ",calculate_power_UFC_MMA_1(0,50/3.6,1.225)*7)
    print("UFC-MMA-2 Quadcopter Energy (Wh): ",calculate_power_UFC_MMA_2(0,50/3.6,1.225)*7)
    print("UFC-MMA-3 Osprey Energy (Wh): ",calculate_power_UFC_MMA_3(0,50/3.6,1.225)*7)
    print("UFC-MMA-4 Yangda Energy (wh): ",calculate_power_UFC_MMA_4(0,50/3.6,1.225)*7)