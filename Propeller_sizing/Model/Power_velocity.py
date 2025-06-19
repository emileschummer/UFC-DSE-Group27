import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
import pandas as pd
from Propeller_sizing.Model.UFC_FC_YEAH import *
import Propeller_sizing.Input.Strava_input_csv as sva
from statistics import mode, StatisticsError
W= 250
S_wing = 2
CLmax = 2
V_vert_prop = 11
numberengines_vertical = 4
numberengines_horizontal = 1
propeller_wake_efficiency = 0.7
L_blade = 0.7366
w_blade = 0.075
L_stab= 0.6
w_stab= 0.5
L_poles= 3.6*L_blade/2 + 0.5
w_poles= 0.34
L_motor = 0.3
L_gimbal = 0.12
L_speaker = 0.1

L_n = 0.2
L_c = 0.6
L_fus = 2*L_n + L_c
w_fus = S_wing / L_fus
d_fus = 0.25

aero_df = pd.read_csv('Propeller_sizing/Model/aero.csv')

races = sva.make_race_dictionnary()
df_vertical = pd.read_csv('Propeller_sizing/Input/Prop_Engine_Data/UAV_Propellers_and_Motor_Specs_Vertical.csv')
df_vertical['Thrust_N']= df_vertical[' Thrust_g '] * g /1000
df_horizontal = pd.read_csv('Propeller_sizing/Input/Prop_Engine_Data/UAV_Propellers_and_Motor_Specs_Horizontal.csv')
df_horizontal['Thrust_N']= df_horizontal[' Thrust_g '] * g /1000

def power_V():
    for race_name, race_data in races.items():
        P_list= []
        velocity_list = []
        t = 0
        prev_velocity = 0 
        prev_grade_smooth = 0
        
        for index, row in race_data.iterrows():
            time = row[" time"]  
            velocity_smooth = row[" velocity_smooth"]
            grade_smooth = np.arctan(row[" grade_smooth"] / 100)
            altitude = row[" altitude"]
            rho = sva.air_density_isa(altitude)
            
            # Calculate acceleration
            time_diff = time - t
            if t > 0:
                acceleration = (velocity_smooth - prev_velocity) / time_diff
                pitch_rate = (grade_smooth - prev_grade_smooth) / time_diff
            else:
                acceleration = 0
                pitch_rate = 0
            prev_velocity = velocity_smooth
            prev_grade_smooth = grade_smooth
            t = time
            P= calculate_power_FC(df_vertical,df_horizontal,grade_smooth,velocity_smooth,rho, acceleration, pitch_rate, W, V_vert_prop, CLmax, S_wing, aero_df, numberengines_vertical,numberengines_horizontal, propeller_wake_efficiency,L_fus,L_n,L_c, w_fus, d_fus,L_blade,L_stab, L_poles, w_poles,L_speaker, L_gimbal, L_motor)
            velocity_list.append(velocity_smooth)
            P_list.append(P)

        df_power_velocity = pd.DataFrame({'Power': P_list, 'Velocity': velocity_list})

        df_power_vs_velocity = df_power_velocity.groupby('Velocity')['Power'].mean().sort_index()
        
        # Create the plot
        plt.figure(figsize=(10, 6))
        plt.plot(df_power_vs_velocity.index, df_power_vs_velocity.values)
        plt.xlabel('Velocity (m/s)')
        plt.ylabel('Power (W)')
        plt.title(f'Power vs Velocity - {race_name}')
        plt.grid(True)
        plt.show()

        

    

