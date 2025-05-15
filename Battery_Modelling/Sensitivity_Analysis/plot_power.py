import sys
import os

# Add the parent directory of 'Battery_Modelling' to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))


import matplotlib.pyplot as plt
from math import ceil
import os
from datetime import datetime

from Battery_Modelling.Modelling.UFC_MMA_1_Helicopter import *
from Battery_Modelling.Modelling.UFC_MMA_2_Quad import *
from Battery_Modelling.Modelling.UFC_MMA_3_Osprey import *
from Battery_Modelling.Modelling.UFC_MMA_4_Yangda import *
from Battery_Modelling.Input.Configuration_inputs import *
from Battery_Modelling.Input import Strava_input_csv as sva


def plot_power_vs_velocity_sensitivity(folder,slope=0, iterations = 100, variance = 0.1, show = False):
    velocity = np.linspace(0,40,1000)
    slope *= np.pi / 180
    inputs_list_original = [[W, eta, CD_MMA1, S_MMA1, diameter_MMA1, A_MMA1],
                            [W, eta, CD_MMA2, Stop_MMA2, Sfront_MMA2, totalA_MMA2],
                            [W, eta, CD0_MMA3, piAe_MMA3, S_MMA3, CLmax_MMA3, r_MMA3],
                            [W, eta, CD0_MMA4, piAe_MMA4, S_MMA4, CLmax_MMA4, r_MMA4, prop_efficiency_MMA4]]
    for i in range(iterations):
        inputs_list = []
        for inputs in inputs_list_original:
            modified_inputs = [value * (1 + np.random.uniform(-variance, variance)) for value in inputs]
            inputs_list.append(modified_inputs)
        T = [[], [], [], []]
        for v in velocity:
            T1 = calculate_power_UFC_MMA_1(slope, v, 1.225, inputs_list[0])
            T2 = calculate_power_UFC_MMA_2(slope, v, 1.225, inputs_list[1])
            T3 = calculate_power_UFC_MMA_3(slope, v, 1.225, inputs_list[2])
            T4 = calculate_power_UFC_MMA_4(slope, v, 1.225, inputs_list[3])
            T[0].append(T1)
            T[1].append(T2)
            T[2].append(T3)
            T[3].append(T4)
        if i == 0:
            plt.plot(velocity, T[0], label='Helicopter', color='blue')
            plt.plot(velocity, T[1], label='Quadcopter', color='orange')
            plt.plot(velocity, T[2], label='Osprey', color='green')
            plt.plot(velocity, T[3], label='Yangda', color='red')
        plt.plot(velocity, T[0], color='blue')
        plt.plot(velocity, T[1], color='orange')
        plt.plot(velocity, T[2], color='green')
        plt.plot(velocity, T[3], color='red')
    plt.legend()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = os.path.join(folder, f"power_vs_velocity_sensitivity_at_{slope}_slope_{timestamp}.png")
    plt.savefig(output_path)
    if show:  plt.show()
    plt.close()


def get_race_results(folder, iterations=100, variance=0.1):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = os.path.join(folder, f"race_results_{timestamp}.txt")
    
    with open(output_file, "w") as file:
        races = sva.make_race_dictionnary()
        race_results = {}
        race_times = {}
        max_energies = [0, 0, 0, 0]
        
        for race_name, race_data in races.items():
            file.write(f"\n\n---------{race_name}------------------------------------------------------\n")
            print(f"\n---------{race_name}---------\n")
            race_times[race_name] = race_data[" time"].max()
            file.write(f"Race time: {round(race_times[race_name]/3600, 2)}h\n")
                        # Highlight regions where speed > 15 m/s
            speed_count = 0
            speed_plot = race_data[" velocity_smooth"]
            for j in range(len(speed_plot) - 1):
                if speed_plot[j] > 15:
                    speed_count+=1
            file.write(f"Maximum speed: {max(speed_plot)} m/s\n")
            file.write(f"Speed < 15 m/s (~stall): {1-speed_count/len(speed_plot)} of time\n")
            inputs_list_original = [[W, eta, CD_MMA1, S_MMA1, A_MMA1],
                                    [W, eta, CD_MMA2, Stop_MMA2, Sfront_MMA2, totalA_MMA2],
                                    [W, eta, CD0_MMA3, piAe_MMA3, S_MMA3, CLmax_MMA3, r_MMA3],
                                    [W, eta, CD0_MMA4, piAe_MMA4, S_MMA4, CLmax_MMA4, r_MMA4, prop_efficiency_MMA4]]
            
            for j in range(iterations):
                print(f"\r {int((j+1)/iterations*100)}%", end="")
                inputs_list = []
                for inputs in inputs_list_original:
                    modified_inputs = [value * (1 + np.random.uniform(-variance, variance)) for value in inputs]
                    inputs_list.append(modified_inputs)
                
                for i in range(4):
                    if i == 0:
                        calculate_power = calculate_power_UFC_MMA_1
                        label = 'Helicopter'
                        inputs = inputs_list[0]
                    elif i == 1:
                        calculate_power = calculate_power_UFC_MMA_2
                        label = 'Quadcopter'
                        inputs = inputs_list[1]
                    elif i == 2:
                        calculate_power = calculate_power_UFC_MMA_3
                        label = 'Osprey'
                        inputs = inputs_list[2]
                    elif i == 3:
                        calculate_power = calculate_power_UFC_MMA_4
                        label = 'Yangda'
                        inputs = inputs_list[3]
                        high_speed_energy_count = 0
                    
                    energy = 0
                    t = 0
                    for index, row in race_data.iterrows():
                        time = row[" time"]
                        velocity_smooth = row[" velocity_smooth"]
                        grade_smooth = np.arctan(row[" grade_smooth"] / 100)
                        altitude = row[" altitude"]
                        rho = sva.air_density_isa(altitude)
                        P = calculate_power(grade_smooth, velocity_smooth, rho, inputs)
                        time_diff = time - t
                        energy += time_diff * P
                        t = time
                        if i == 3 and velocity_smooth > 15:
                            high_speed_energy_count += P * time_diff
                    
                    if race_name not in race_results:
                        race_results[race_name] = [[0] * iterations for _ in range(4)]
                    race_results[race_name][i][j] = energy / 3600  # Store energy in Wh
            
            for k in range(4):
                file.write(f"\n---------UFC-MMA-{k+1}---------\n")
                max_energy = max(race_results[race_name][k])
                max_energy_7_hour_race = max_energy/ (race_times[race_name]/3600)*7
                if max_energy_7_hour_race > max_energies[k]:
                    max_energies[k] = max_energy_7_hour_race
                file.write(f"Average energy consumption through iterations: {np.mean(race_results[race_name][k])} Wh\n")
                file.write(f"Maximum energy consumption through iterations: {max_energy} Wh\n")
                file.write(f"Maximum energy consumption through iterations for a 7h race: {max_energy_7_hour_race} Wh/h")
                
        file.write("\n\n------------------------------------------------------------------------------------\n")
        file.write("---------Summary--------------------------------------------------------------------\n")
        for l in range(4):
            file.write(f"---------UFC-MMA-{l+1}---------\n")
            file.write(f"Maximum energy consumption per hour for a 7h race: {max_energies[l]} Wh/h\n")
            file.write(f"Drones required for 7h of filming (2250Wh per drone): {ceil(max_energies[l]/2250)}\n")
    print("\n Done")