import numpy as np
from matplotlib import pyplot as plt
import aerosandbox as asb
import pandas as pd
import os


#run this per alpha to get the half span load distribution at that alpha
#es// distribution_alpha0 = load_distribution_halfspan(wing_geom, lift_distribution, alpha=0, half_span=1.5, plot = False)

def load_distribution_halfspan(wing_geom, lift_distribution, alpha, half_span=1.5, plot = False,output_folder = "Final_UAV_Sizing/Output/Wing_Sizing" ):

    slice_locations_xyz_le = [xsec.xyz_le for xsec in wing_geom.xsecs]
    y_values = [axis[1] for axis in slice_locations_xyz_le]
    
    index = lift_distribution["alpha"].index(alpha)

    # Calculate midpoints between consecutive y-values
    y_midpoints = np.array([(y1 + y2) / 2 for y1, y2 in zip(y_values[:-1], y_values[1:])])
    div = y_midpoints / float(half_span)
    distribution = [div, lift_distribution["CLs"][index]]

    if plot:
        plt.figure()
        plt.plot(div, lift_distribution["CLs"][index], label=f'alpha {lift_distribution["alpha"][index]}')
        plt.xlabel("x/b/2")
        plt.ylabel("Lift")
        plt.legend()
        plt.grid(True)
        plt.title(f"Lift Distribution alpha {lift_distribution['alpha'][index]}")
        plot_path = os.path.join(output_folder, f"lift_distribution_alpha_{lift_distribution['alpha'][index]}.png")
        plt.savefig(plot_path)
        plt.show()
        plt.close()
    

    return distribution

