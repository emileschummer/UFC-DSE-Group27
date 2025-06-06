import numpy as np 
import aerosandbox as AS

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


def Rotate_for_Inertia(coordinates,name,angle):
    # coordinates = load_airfoil_dat(r"C:\Users\marco\Documents\GitHub\UFC-DSE-Group27\AerodynamicDesign\AirfoilData\Airfoil.dat")
    # name = "S1223"
    my_airfoil = AS.Airfoil(name=name, coordinates=coordinates)
    Rotated_airfoil = my_airfoil.rotate(angle)

    # print(Rotated_airfoil)
    # print(Rotated_airfoil.coordinates)

    return Rotated_airfoil.coordinates
 



def Airfoil_Moment_of_Inertia(points,Length):
    # Replace with your array if reading from a file
    #points = load_airfoil_dat("Structural Sizing\AirfoilData\Airfoil.dat")
    # points = np.array([ 1.0000e+00,  0.0000e+00]
    #  [ 9.9838e-01,  1.2600e-03]
    #  [ 9.9417e-01,  4.9400e-03]
    #  [ 9.8825e-01,  1.0370e-02]
    #  [ 9.8075e-01,  1.6460e-02]
    #  [ 9.7111e-01,  2.2500e-02]
    #  [ 9.5884e-01,  2.8530e-02]
    #  [ 9.4389e-01,  3.4760e-02]
    #  [ 9.2639e-01 , 4.1160e-02]
    #  [ 9.0641e-01,  4.7680e-02]
    #  [ 8.8406e-01,  5.4270e-02]
    #  [ 8.5947e-01,  6.0890e-02]
    #  [ 8.3277e-01,  6.7490e-02]
    #  [ 8.0412e-01,  7.4020e-02]
    #  [ 7.7369e-01,  8.0440e-02]
    #  [ 7.4166e-01,  8.6710e-02]
    #  [ 7.0823e-01,  9.2770e-02]
    #  [ 6.7360e-01,  9.8590e-02]
    #  [ 6.3798e-01,  1.0412e-01]
    #  [ 6.0158e-01,  1.0935e-01]
    #  [ 5.6465e-01,  1.1425e-01]
    #  [ 5.2744e-01,  1.1881e-01]
    #  [ 4.9025e-01,  1.2303e-01]
    #  [ 4.5340e-01,  1.2683e-01]
    #  [ 4.1721e-01,  1.3011e-01]
    #  [ 3.8193e-01,  1.3271e-01]
    #  [ 3.4777e-01,  1.3447e-01]
    #  [ 3.1488e-01,  1.3526e-01]
    #  [ 2.8347e-01,  1.3505e-01]
    #  [ 2.5370e-01,  1.3346e-01]
    #  [ 2.2541e-01,  1.3037e-01]
    #  [ 1.9846e-01,  1.2594e-01]
    #  [ 1.7286e-01,  1.2026e-01]
    #  [ 1.4863e-01,  1.1355e-01]
    #  [ 1.2591e-01,  1.0598e-01]
    #  [ 1.0482e-01,  9.7700e-02]
    #  [ 8.5450e-02,  8.8790e-02]
    #  [ 6.7890e-02,  7.9400e-02]
    #  [ 5.2230e-02,  6.9650e-02]
    #  [ 3.8550e-02,  5.9680e-02]
    #  [ 2.6940e-02,  4.9660e-02]
    #  [ 1.7550e-02,  3.9610e-02]
    #  [ 1.0280e-02,  2.9540e-02]
    #  [ 4.9500e-03,  1.9690e-02]
    #  [ 1.5500e-03,  1.0330e-02]
    #  [ 5.0000e-05,  1.7800e-03]
    #  [ 4.4000e-04, -5.6100e-03]
    #  [ 2.6400e-03, -1.1200e-02]
    #  [ 7.8900e-03, -1.4270e-02]
    #  [ 1.7180e-02, -1.5500e-02]
    #  [ 3.0060e-02, -1.5840e-02]
    #  [ 4.6270e-02, -1.5320e-02]
    #  [ 6.5610e-02, -1.4040e-02]
    #  [ 8.7870e-02, -1.2020e-02]
    #  [ 1.1282e-01, -9.2500e-03]
    #  [ 1.4020e-01, -5.6300e-03]
    #  [ 1.7006e-01, -7.5000e-04]
    #  [ 2.0278e-01,  5.3500e-03]
    #  [ 2.3840e-01,  1.2130e-02]
    #  [ 2.7673e-01,  1.9280e-02]
    #  [ 3.1750e-01,  2.6520e-02]
    #  [ 3.6044e-01,  3.3580e-02]
    #  [ 4.0519e-01,  4.0210e-02]
    #  [ 4.5139e-01,  4.6180e-02]
    #  [ 4.9860e-01,  5.1290e-02]
    #  [ 5.4639e-01,  5.5340e-02]
    #  [ 5.9428e-01,  5.8200e-02]
    #  [ 6.4176e-01 , 5.9760e-02]
    #  [ 6.8832e-01 , 5.9940e-02]
    #  [ 7.3344e-01 , 5.8720e-02]
    #  [ 7.7660e-01,  5.6120e-02]
    #  [ 8.1729e-01,  5.2190e-02]
    #  [ 8.5500e-01,  4.7060e-02]
    #  [ 8.8928e-01,  4.0880e-02]
    #  [ 9.1966e-01,  3.3870e-02]
    #  [ 9.4573e-01,  2.6240e-02]
    #  [ 9.6693e-01,  1.8220e-02]
    #  [ 9.8255e-01,  1.0600e-02]
    #  [ 9.9268e-01,  4.6800e-03]
    #  [ 9.9825e-01,  1.1500e-03]
    #  [ 1.0000e+00,  0.0000e+00])

    # Ensure it's closed
    if not np.allclose(points[0], points[-1]):
        points = np.vstack([points, points[0]])

    x = points[:, 0]*Length
    y = points[:, 1]*Length

    # Shoelace helper
    def poly_area(x, y):
        return 0.5 * np.sum(x[:-1]*y[1:] - x[1:]*y[:-1])

    A = poly_area(x, y)

    # Common factor
    cross = x[:-1]*y[1:] - x[1:]*y[:-1]

    Ixx = (1/12) * np.sum((y[:-1]**2 + y[:-1]*y[1:] + y[1:]**2) * cross)
    Iyy = (1/12) * np.sum((x[:-1]**2 + x[:-1]*x[1:] + x[1:]**2) * cross)
    Ixy = (1/24) * np.sum((x[:-1]*y[1:] + 2*x[:-1]*y[:-1] + 2*x[1:]*y[1:] + x[1:]*y[:-1]) * cross)

    # Optionally divide by area to get centroid location:
    Cx = (1/(6*A)) * np.sum((x[:-1] + x[1:]) * cross)
    Cy = (1/(6*A)) * np.sum((y[:-1] + y[1:]) * cross)

    # Parallel axis theorem to shift to centroid
    Ixx_c = Ixx - A * Cy**2
    Iyy_c = Iyy - A * Cx**2
    Ixy_c = Ixy - A * Cx * Cy

    print(f"Area A = {A:.6e}")
    print(f"Centroid: ({Cx:.6e}, {Cy:.6e})")
    print(f"Ixx (centroidal) = {Ixx_c:.6e}")
    print(f"Iyy (centroidal) = {Iyy_c:.6e}")
    print(f"Ixy (centroidal) = {Ixy_c:.6e}")

    return Ixx_c,Iyy_c,Ixy_c
