import numpy as np 
from aerosandbox import OperatingPoint


def load_airfoil_dat(path):
    with open(path, "r") as f:
        lines = f.readlines()
    coords = []
    for line in lines:
        parts = line.strip().split()
        if len(parts) == 2:
            try:
                x, y = float(parts[0]), float(parts[1])
                coords.append([x, y])
            except ValueError:
                continue
    return np.array(coords)
