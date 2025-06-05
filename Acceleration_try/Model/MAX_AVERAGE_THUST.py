import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import numpy as np
import Acceleration_try.Input.Config as config
from Acceleration_try.Model.UFC_FC_YEAH import *
import Acceleration_try.Input.Strava_input_csv as sva



races = sva.make_race_dictionnary()
inputs = config.input_list_final
for race_name, race_data in races.items():
    
    Tverttical_list= []
    Thorizontal_list = []
    calculate_power = calculate_power_UFC_FC
    t = 0
    prev_velocity = 0 
    prev_grade_smooth= 0 
    for index, row in race_data.iterrows():
        time = row[" time"]  
        velocity_smooth = row[" velocity_smooth"]
        grade_smooth = np.arctan(row[" grade_smooth"] / 100)
        altitude = row[" altitude"]
        rho = sva.air_density_isa(altitude)
        
        # Calculate acceleration using current and previous velocity
        time_diff = time - t
        if t > 0:  # Skip first point
            acceleration = (velocity_smooth - prev_velocity) / time_diff
            pitch_rate = (grade_smooth - prev_grade_smooth) / time_diff  # Calculate pitch rate
        else:
            acceleration = 0
            pitch_rate = 0
        prev_velocity = velocity_smooth # Store current velocity for next iteration
        prev_grade_smooth = grade_smooth  # Store current grade for next iteration
        t = time

        Tvertical, Thorizontal = calculate_power(grade_smooth, velocity_smooth, rho, inputs, acceleration, pitch_rate)
        Tverttical_list.append(Tvertical)
        Thorizontal_list.append(Thorizontal)
    # Print maximum and average thrusts for this race
    print(f"\nRace: {race_name}")
    print(f"Maximum absolute vertical thrust: {max(abs(np.array(Tverttical_list))):.2f} N")
    print(f"Average vertical thrust: {sum(Tverttical_list)/len(Tverttical_list):.2f} N")
    print(f"Maximum absolute horizontal thrust: {max(abs(np.array(Thorizontal_list))):.2f} N")
    print(f"Average horizontal thrust: {sum(Thorizontal_list)/len(Thorizontal_list):.2f} N")
    
    # Plot thrusts against time
    import matplotlib.pyplot as plt
    
    time_points = race_data[' time'].values
    plt.figure(figsize=(10, 6))
    #plt.plot(time_points, Tverttical_list, label='Vertical Thrust')
    plt.plot(time_points, Thorizontal_list, label='Horizontal Thrust')
    plt.xlabel('Time (s)')
    plt.ylabel('Thrust (N)')
    plt.title(f'Thrust vs Time - {race_name}')
    plt.legend()
    plt.grid(True)
    plt.show()