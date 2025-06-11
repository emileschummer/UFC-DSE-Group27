import os
import pandas as pd

def make_race_dictionnary():
    races = {}
    current_dir = os.path.dirname(os.path.abspath(__file__))  # Location of main.py
    data_folder = os.path.join(current_dir, "Data")
    
    if not os.path.exists(data_folder):
        print(f"Data folder {data_folder} does not exist.")
        return {}
    
    for file_name in os.listdir(data_folder):
        if file_name.endswith(".csv"):
            file_path = os.path.join(data_folder, file_name)
            try:
                data = pd.read_csv(file_path)
                races[file_name] = data
            except Exception as e:
                print(f"Error processing file {file_name}: {e}") 
    return races

def air_density_isa(h):
    T0 = 288.15  # Sea level standard temperature (K)
    p0 = 101325  # Sea level standard pressure (Pa)
    L = -0.0065  # Temperature lapse rate (K/m)
    g = 9.80665  # Gravity (m/s^2)
    R = 287.058  # Specific gas constant for air (J/kg·K)

    T = T0 + L * h
    p = p0 * (T / T0) ** (-g / (L * R))
    rho = p / (R * T)

    return rho
def altitude_from_density(rho):
    T0 = 288.15  # Sea level standard temperature (K)
    p0 = 101325  # Sea level standard pressure (Pa)
    L = -0.0065  # Temperature lapse rate (K/m)
    g = 9.80665  # Gravity (m/s^2)
    R = 287.058  # Specific gas constant for air (J/kg·K)

    # Rearranged ISA formula to solve for h given rho
    # rho = p0 / (R * T0) * (1 + (L * h) / T0) ** (-(g / (L * R) + 1))
    # Let A = -(g / (L * R) + 1)
    A = -(g / (L * R) + 1)
    rho0 = p0 / (R * T0)
    ratio = rho / rho0
    # (1 + (L * h) / T0) = ratio ** (1 / A)
    temp = ratio ** (1 / A)
    h = (temp - 1) * T0 / L
    return h

