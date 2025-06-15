import numpy as np
from matplotlib import pyplot as plt
import aerosandbox as asb
import pandas as pd


#run this per alpha to get the half span load distribution at that alpha
#es// distribution_alpha0 = load_distribution_halfspan(wing_geom, lift_distribution, alpha=0, half_span=1.5, plot = False)

def load_distribution_halfspan(wing_geom, lift_distribution, alpha, half_span=1.575, plot = False):

    slice_locations_xyz_le = [xsec.xyz_le for xsec in wing_geom.xsecs]
    y_values = [axis[1] for axis in slice_locations_xyz_le]
    
    index = lift_distribution["alpha"].index(alpha)

    # Calculate midpoints between consecutive y-values
    y_midpoints = np.array([(y1 + y2) / 2 for y1, y2 in zip(y_values[:-1], y_values[1:])])
    
    distribution = [y_midpoints / half_span, lift_distribution["CLs"][index]]
    print(y_midpoints/ half_span)

    if plot == True: 
        plt.figure()
        plt.plot(y_midpoints / half_span, lift_distribution["CLs"][index], label=f'alpha {lift_distribution["alpha"][index]}')
        plt.xlabel("x/b/2")
        plt.ylabel("Lift")
        plt.legend()
        plt.grid(True)
        plt.title(f"Lift Distribution alpha {lift_distribution['alpha'][index]}")
        plt.show()

    return distribution

