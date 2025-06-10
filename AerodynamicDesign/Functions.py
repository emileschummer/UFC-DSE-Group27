import numpy as np 
import aerosandbox as asb


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

def wing_geometry_calculator(InputWeight, alpha, csv, velocity_op, altitude, taper_ratio, b):
    #from csv should take the CL assosciated to the alpha that want to analyse. it should take the old CL.
    
    op_point_for_atmo = asb.OperatingPoint(velocity=velocity_op, atmosphere=asb.Atmosphere(altitude=altitude))
    rho = op_point_for_atmo.atmosphere.density()

    S = InputWeight/(0.5*rho*velocity_op**2*CL)
    
    cr = 4*S/(b*(1 + taper_ratio))

    ct = cr*taper_ratio

    return S, cr, ct