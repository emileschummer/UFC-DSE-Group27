import pandas as pd
import numpy as np

df= pd.read_csv('Battery_Modelling/Input/Data/WVA_Giro_Stage1.csv')

time= df[' time'].values
distance= df[' distance'].values
velocity= df[' velocity_smooth'].values
altitude= df[' altitude'].values
gradient= df[' grade_smooth'].values

def air_density_isa(h):
    T0 = 288.15  # Sea level standard temperature (K)
    p0 = 101325  # Sea level standard pressure (Pa)
    L = -0.0065  # Temperature lapse rate (K/m)
    g = 9.80665  # Gravity (m/s^2)
    R = 287.058  # Specific gas constant for air (J/kg·K)

    # Temperature at altitude h
    T = T0 + L * h

    # Pressure at altitude h
    p = p0 * (T / T0) ** (-g / (L * R))

    # Density at altitude h
    rho = p / (R * T)

    return rho

density=[]

for alt in altitude:
    rho = air_density_isa(alt)
    density.append(rho)

inclination = []
for inc in gradient:
    angle= np.arctan(inc/100)
    inclination.append(angle)


