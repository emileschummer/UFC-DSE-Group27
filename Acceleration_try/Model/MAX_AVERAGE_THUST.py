import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import numpy as np
import pandas as pd
import Acceleration_try.Input.Config as config
from Acceleration_try.Model.UFC_FC_YEAH import calculate_thrust_UFC_FC
from statistics import mode, StatisticsError
import Acceleration_try.Input.Strava_input_csv as sva


races = sva.make_race_dictionnary()
inputs = config.input_list_final
for race_name, race_data in races.items():
    
    Tvertical_list= []
    Thorizontal_list = []
    calculate_thrust = calculate_thrust_UFC_FC
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

        Tvertical, Thorizontal = calculate_thrust(grade_smooth, velocity_smooth, rho, inputs, acceleration, pitch_rate)
        Tvertical_list.append(Tvertical)
        Thorizontal_list.append(Thorizontal)
    # Print maximum and average thrusts for this race
   
    non_zero_vertical = [t for t in Tvertical_list if t != 0]
    non_negative_horizontal = [t for t in Thorizontal_list if t >= 0]
    print(f"\nRace: {race_name}")
    print(f"Maximum absolute vertical thrust: {max(abs(np.array(Tvertical_list))):.2f} N")
    print(f"Maximum absolute horizontal thrust: {max(abs(np.array(Thorizontal_list))):.2f} N")
    print(f"Average vertical thrust (excluding zeros): {sum(non_zero_vertical)/len(non_zero_vertical):.2f} N")
    print(f"Average horizontal thrust (excluding negative): {sum(non_negative_horizontal)/len(non_negative_horizontal):.2f} N")
    try:
        # Filter out zero values from Tvertical_list
        print(f"Most common vertical thrust value (excluding zeros): {mode(non_zero_vertical):.2f} N")
        print(f"Most common horizontal thrust value (excluding negative): {mode(Thorizontal_list):.2f} N")
    except StatisticsError:
        print("No unique mode found for thrust values")
    
    
    # Plot thrusts against time
    import matplotlib.pyplot as plt
    
    time_points = race_data[' time'].values
    plt.figure(figsize=(10, 6))
    plt.plot(time_points, Tvertical_list, label='Vertical Thrust')
    plt.plot(time_points, Thorizontal_list, label='Horizontal Thrust')
    plt.xlabel('Time (s)')
    plt.ylabel('Thrust (N)')
    plt.title(f'Thrust vs Time - {race_name}')
    plt.legend()
    plt.grid(True)
    #plt.show()