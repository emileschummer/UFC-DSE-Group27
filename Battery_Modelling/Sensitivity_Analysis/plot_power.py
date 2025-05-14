import sys
import os

# Add the parent directory of 'Battery_Modelling' to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))


import matplotlib.pyplot as plt

from Battery_Modelling.Modelling.UFC_MMA_1_Helicopter import *
from Battery_Modelling.Modelling.UFC_MMA_2_Quad import *
from Battery_Modelling.Modelling.UFC_MMA_3_Osprey import *
from Battery_Modelling.Modelling.UFC_MMA_4_Yangda import *
from Battery_Modelling.Input.Configuration_inputs import *
from Battery_Modelling.Input import Strava_input_csv as sva

def plot_power_vs_velocity_sensitivity(slope=0, iterations = 100, variance = 0.1):
    velocity = np.linspace(0,40,1000)
    slope*=np.pi/180
    inputs_list_original = [[W,eta,CD_MMA1,S_MMA1,A_MMA1],
                   [W, eta, CD_MMA2, Stop_MMA2, Sfront_MMA2, totalA_MMA2],
                   [W, eta, CD0_MMA3, piAe_MMA3, S_MMA3, CLmax_MMA3, r_MMA3],
                   [W, eta, CD0_MMA4, piAe_MMA4, S_MMA4, CLmax_MMA4, r_MMA4, prop_efficiency_MMA4]]
    for i in range(iterations):
        inputs_list = []
        for inputs in inputs_list_original:
            modified_inputs = [value * (1 + np.random.uniform(-variance, variance)) for value in inputs]
            inputs_list.append(modified_inputs)
        T = [[],[],[],[]]
        for v in velocity:
            T1 = calculate_power_UFC_MMA_1(slope,v,1.225,inputs_list[0])
            T2 = calculate_power_UFC_MMA_2(slope,v,1.225,inputs_list[1])
            T3 = calculate_power_UFC_MMA_3(slope,v,1.225,inputs_list[2])
            T4 = calculate_power_UFC_MMA_4(slope,v,1.225,inputs_list[3])
            T[0].append(T1)
            T[1].append(T2)
            T[2].append(T3)
            T[3].append(T4)
        if i == 0:
            plt.plot(velocity,T[0],label = 'Helicopter', color = 'blue')
            plt.plot(velocity,T[1], label = 'Quadcopter', color = 'orange')
            plt.plot(velocity,T[2], label = 'Osprey', color = 'green')
            plt.plot(velocity,T[3], label = 'Yangda', color = 'red')
        plt.plot(velocity,T[0], color = 'blue')
        plt.plot(velocity,T[1], color = 'orange')
        plt.plot(velocity,T[2], color = 'green')
        plt.plot(velocity,T[3], color = 'red')

    plt.legend()
    plt.show()
def get_race_results(iterations = 100, variance = 0.1):
    races = sva.make_race_dictionnary()
    race_results = {}
    for race_name, race_data in races.items():
        print(f'---------{race_name}---------')
        inputs_list_original = [[W,eta,CD_MMA1,S_MMA1,A_MMA1],
                   [W, eta, CD_MMA2, Stop_MMA2, Sfront_MMA2, totalA_MMA2],
                   [W, eta, CD0_MMA3, piAe_MMA3, S_MMA3, CLmax_MMA3, r_MMA3],
                   [W, eta, CD0_MMA4, piAe_MMA4, S_MMA4, CLmax_MMA4, r_MMA4, prop_efficiency_MMA4]]
        for j in range(iterations):
            inputs_list = []
            for inputs in inputs_list_original:
                modified_inputs = [value * (1 + np.random.uniform(-variance, variance)) for value in inputs]
                inputs_list.append(modified_inputs)
            for i in range(4):
                race_plot = []
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
                    time = row[" time"]  # Access directly from DataFrame row
                    velocity_smooth = row[" velocity_smooth"]
                    grade_smooth = np.arctan(row[" grade_smooth"] / 100)
                    altitude = row[" altitude"]
                    rho = sva.air_density_isa(altitude)
                    P = calculate_power(grade_smooth, velocity_smooth, rho, inputs)
                    time_diff = time - t
                    energy = energy + time_diff * P
                    t = time
                    if i == 3: #Analysing yangda
                        if velocity_smooth > 15:
                            high_speed_energy_count += P * time_diff
                if race_name not in race_results:
                    race_results[race_name] = [[0] * iterations for _ in range(4)]
                race_results[race_name][i][j] = energy / 3600/iterations  # Store energy in Wh
        for i in range(4):
            print(f'---------UFC-MMA-{i+1}---------')
            print(f"Maximum energy consumption: {max(race_results[race_name][i])} Wh")
            print(f"Average energy consumption: {np.mean(race_results[race_name][i])} Wh")  
