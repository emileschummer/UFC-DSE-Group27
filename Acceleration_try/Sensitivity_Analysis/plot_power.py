import sys
import os

# Add the parent directory of 'Battery_Modelling' to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))


import matplotlib.pyplot as plt
from math import ceil
import os
from datetime import datetime

from Model.UFC_FC_YEAH import *
from Input.Config import *
import Input.Strava_input_csv as sva


def plot_power_vs_velocity_sensitivity(folder,slope=0, iterations = 100, variance = 0.1, show = False):
    print(f"---------Plot Power vs Velocity---------")
    velocity = np.linspace(0,40,1000)
    slope *= np.pi / 180
    V_stall = input_list_final[9]
    for i in range(iterations):
        inputs_list = []
        for inputs in inputs_list_original:
            modified_inputs = [value * (1 + np.random.uniform(-variance, variance)) for value in inputs]
            inputs_list.append(modified_inputs)
        T = []
        for v in velocity:
            T = calculate_power_UFC_FC(slope, v, 1.225, input_list_final, )
            T.append(T)
        if i == 0:
            plt.axvline(x=V_stall, color='black', linestyle='--', label=f'Stall Speed ({V_stall:.2f} m/s)')
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
    output_path = os.path.join(folder, f"Power_vs_velocity_sensitivity_at_{slope}_slope_{timestamp}.png")
    plt.savefig(output_path)
    if show:  
        print("Close plot to continue")
        plt.show()
    plt.close()
    print("Done")


def get_race_results(folder, battery_capacity=2250, iterations=100, variance=0.1):
    print(f"---------Compute Race Results---------")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = os.path.join(folder, f"race_results_{timestamp}.txt")
    
    with open(output_file, "w") as file:
        V_stall = input_list_final[9]
        file.write(f"Stall Speed: {V_stall} m/s or {V_stall*3.6} km/h\n")
        print(f"Stall Speed: {V_stall} m/s or {V_stall*3.6} km/h\n")
        races = sva.make_race_dictionnary()
        race_results = {}
        race_times = {}
        max_energy = 0
        av_energy = 0
        
        for race_name, race_data in races.items():
            file.write(f"\n\n---------{race_name}------------------------------------------------------\n")
            print(f"\n---------{race_name}---------\n")
            race_times[race_name] = race_data[" time"].max()
            file.write(f"Race time: {round(race_times[race_name]/3600, 2)}h\n")
            speed_count = 0
            speed_plot = race_data[" velocity_smooth"]
            
            for j in range(len(speed_plot) - 1):
                if speed_plot[j] > V_stall:
                    speed_count+=1
            file.write(f"Maximum speed: {max(speed_plot)} m/s\n")
            file.write(f"Speed < {V_stall} m/s (~stall): {1-speed_count/len(speed_plot)} of time\n")
            
            if race_name not in race_results:
                race_results[race_name] = [0] * iterations
                
            for j in range(iterations):
                print(f"\r {int((j+1)/iterations*100)}%", end="")
                inputs_list = []
                for inputs in inputs_list_original:
                    modified_inputs = [value * (1 + np.random.uniform(-variance, variance)) for value in inputs]
                    inputs_list.append(modified_inputs)
                
                energy = 0
                t = 0
                prev_velocity = 0 
                prev_grade_smooth= 0
                for index, row in race_data.iterrows():
                    time = row[" time"]
                    velocity_smooth = row[" velocity_smooth"]
                    grade_smooth = np.arctan(row[" grade_smooth"] / 100)
                    altitude = row[" altitude"]
                    rho = sva.air_density_isa(altitude)
                    time_diff = time - t
                    if t > 0:
                        acceleration = (velocity_smooth - prev_velocity) / time_diff
                        pitch_rate = (grade_smooth - prev_grade_smooth) / time_diff

                    else:
                        acceleration = 0
                        pitch_rate = 0
                    P = calculate_power_UFC_FC(grade_smooth, velocity_smooth, rho, input_list_final, acceleration, pitch_rate)  # Using Yangda-style inputs
                    energy += time_diff * P
                    t = time
                
                race_results[race_name][j] = energy / 3600  # Store energy in Wh
            
            current_max = max(race_results[race_name])
            max_energy_7_hour = current_max / (race_times[race_name]/3600) * 7
            current_av = np.mean(race_results[race_name]) / (race_times[race_name]/3600) * 7
            
            if max_energy_7_hour > max_energy:
                max_energy = max_energy_7_hour
            if current_av > av_energy:
                av_energy = current_av
                
            file.write(f"\n---------Yangda-style---------\n")
            file.write(f"Average energy consumption through iterations: {np.mean(race_results[race_name])} Wh\n")
            file.write(f"Average energy consumption through iterations for a 7h race: {current_av} Wh/7h\n")
            file.write(f"Maximum energy consumption through iterations: {current_max} Wh\n")
            file.write(f"Maximum energy consumption through iterations for a 7h race: {max_energy_7_hour} Wh/7h\n")
        
        file.write("\n\n------------------------------------------------------------------------------------\n")
        file.write("---------Summary--------------------------------------------------------------------\n")
        file.write("---------Yangda-style---------\n")
        file.write(f"Maximum energy consumption for a 7h race: {max_energy} Wh/7h\n")
        file.write(f"Endurance based on maximum: {round(battery_capacity/(max_energy/7), 2)}h\n")
        file.write(f"Relay points required for 7h of filming ({battery_capacity}Wh per drone) based on maximum: {ceil(max_energy/battery_capacity)-1}\n")
        file.write(f"Average energy consumption through iterations for a 7h race: {av_energy} Wh/7h\n")
        file.write(f"Endurance based on average: {round(battery_capacity/(av_energy/7), 2)}h\n")
        file.write(f"Relay points required for 7h of filming ({battery_capacity}Wh per drone) based on average: {ceil(av_energy/battery_capacity)-1}\n")
            
    print("\n Done")
