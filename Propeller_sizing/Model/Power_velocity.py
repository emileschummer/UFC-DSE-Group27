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
d = 0.25

aero_df = pd.read_csv('Propeller_sizing/Model/aero.csv')

races = sva.make_race_dictionnary()
df_vertical = pd.read_csv('Propeller_sizing/Input/Prop_Engine_Data/UAV_Propellers_and_Motor_Specs_Vertical.csv')
df_vertical['Thrust_N']= df_vertical[' Thrust_g '] * g /1000
df_horizontal = pd.read_csv('Propeller_sizing/Input/Prop_Engine_Data/UAV_Propellers_and_Motor_Specs_Horizontal.csv')
df_horizontal['Thrust_N']= df_horizontal[' Thrust_g '] * g /1000

