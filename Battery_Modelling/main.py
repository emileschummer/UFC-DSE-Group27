#from Input.Strava_input import *
from Modelling.UFC_MMA_1_Helicopter import calculate_power_UFC_MMA_1
from Modelling.UFC_MMA_2_Quad import calculate_power_UFC_MMA_2
from Modelling.UFC_MMA_3_Osprey import calculate_power_UFC_MMA_3
from Modelling.UFC_MMA_4_Yangda import calculate_power_UFC_MMA_4
from Input import Strava_input_csv as sva
import sys
import os
"""
#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'C:\\Users\\tijnp\\OneDrive\\Documenten\\Phyton\\DSE\\UFC-DSE-Group27\\Battery_Modelling')))
#from Modelling.DSE_osprey import *


if tijn == True:
    for i in range(4):
        if i == 0:
            calculate_power = calculate_power_UFC_MMA_1
        elif i == 1:
            calculate_power = calculate_power_UFC_MMA_2
        elif i == 2:
            calculate_power = calculate_power_UFC_MMA_3
        elif i == 3:
            calculate_power = calculate_power_UFC_MMA_4
        energy = 0
        t = 0

        for i in data:
            P = calculate_power_UFC_MMA_3(i[2],i[1],i[3])
            time = i[0]-t
            energy = energy + time*P
            t = i[0]
        print(energy , 'J')
        print(energy/3600 , 'Wh')
else:"""
races = sva.make_race_dictionnary()
race_results = {}
for race_name, race_data in races.items():
    for i in range(4):
        if i == 0:
            calculate_power = calculate_power_UFC_MMA_1
        elif i == 1:
            calculate_power = calculate_power_UFC_MMA_2
        elif i == 2:
            calculate_power = calculate_power_UFC_MMA_3
        elif i == 3:
            calculate_power = calculate_power_UFC_MMA_4
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
        print(energy/3600 , 'Wh')
print(race_results)