import numpy as np

from Modelling.UFC_MMA_1_Helicopter import calculate_power_UFC_MMA_1
from Modelling.UFC_MMA_2_Quad import calculate_power_UFC_MMA_2
from Modelling.UFC_MMA_3_Osprey import calculate_power_UFC_MMA_3
from Modelling.UFC_MMA_4_Yangda import calculate_power_UFC_MMA_4
from Input import Strava_input_csv as sva

def get_race_results():
    races = sva.make_race_dictionnary()
    race_results = {}
    for race_name, race_data in races.items():
        for i in range(4):
            if i == 0:
                calculate_power = calculate_power_UFC_MMA_1
                print('Helicopter configuration')
            elif i == 1:
                calculate_power = calculate_power_UFC_MMA_2
                print('Quadcopter configuration')
            elif i == 2:
                calculate_power = calculate_power_UFC_MMA_3
                print('Osprey configuration')
            elif i == 3:
                calculate_power = calculate_power_UFC_MMA_4
                print('Yangda configuration')
            energy = 0
            t = 0
            for index, row in race_data.iterrows():
                time = row[" time"]  # Access directly from DataFrame row
                velocity_smooth = row[" velocity_smooth"]
                grade_smooth = row[" grade_smooth"]
                altitude = row[" altitude"]
                rho = sva.air_density_isa(altitude)
                P = calculate_power(grade_smooth,velocity_smooth,rho)
                time_diff = time - t
                energy = energy + time_diff * P
                t = time
            if race_name not in race_results:
                race_results[race_name] = [0] * 4
            race_results[race_name][i] = energy / 3600  # Store energy in Wh
            print(np.round(energy/3600) , 'Wh')
            print(np.round(energy/(3600*450)), 'kg Li-ion battery') 
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