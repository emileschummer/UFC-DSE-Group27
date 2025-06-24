import matplotlib.pyplot as plt
import numpy as np
import io
import aerosandbox as asb

# Data from the user
data_string = """
Alpha (deg) | CL (VLM) | CD (VLM) | CL (Corrected)
----------------------------------   ------------------------
       -5.0 |  -0.3214 |  0.00187 |      -0.3216
       -4.0 |  -0.2259 |  0.00093 |      -0.2260
       -3.0 |  -0.1303 |  0.00031 |      -0.1304
       -2.0 |  -0.0347 |  0.00002 |      -0.0347
       -1.0 |   0.0610 |  0.00007 |       0.0610
        0.0 |   0.1567 |  0.00046 |       0.1567
        1.0 |   0.2523 |  0.00118 |       0.2524
        2.0 |   0.3478 |  0.00223 |       0.3479
        3.0 |   0.4432 |  0.00361 |       0.4434
        4.0 |   0.5383 |  0.00532 |       0.5387
        5.0 |   0.6332 |  0.00735 |       0.6338
        6.0 |   0.7278 |  0.00969 |       0.7288
        7.0 |   0.8220 |  0.01234 |       0.8235
        8.0 |   0.9159 |  0.01530 |       0.9180
        9.0 |   1.0093 |  0.01854 |       1.0122
       10.0 |   1.1022 |  0.02207 |       1.1061
       11.0 |   1.1947 |  0.02588 |       1.1997
       12.0 |   1.2865 |  0.02994 |       1.2929
       13.0 |   1.3778 |  0.03426 |       1.3237
       14.0 |   1.4684 |  0.03881 |       1.2005
       15.0 |   1.5583 |  0.04359 |       1.0034
       16.0 |   1.6475 |  0.04857 |       0.8707
       17.0 |   1.7360 |  0.05375 |       0.7371
       18.0 |   1.8236 |  0.05911 |       0.6031
       19.0 |   1.9104 |  0.06463 |       0.4688
       20.0 |   1.9963 |  0.07030 |       0.3345
"""

# Read the data into numpy arrays
# We skip the first two header lines and use '|' as the delimiter.
# We are interested in columns 2 (CD) and 3 (CL Corrected).
data = np.genfromtxt(
    io.StringIO(data_string),
    skip_header=3,
    delimiter='|',
    usecols=(2, 3)
)

cd_vlm = data[:, 0]
cl_corrected = data[:, 1]

# Create the plot
plt.figure(figsize=(10, 6))
plt.plot(cl_corrected, cd_vlm, marker='o', linestyle='-', label='CD vs CL')
plt.xlabel("CL")
plt.ylabel("CD")
plt.title("Drag Polar: CD vs CL")
plt.grid(True)
plt.legend()
plt.show()

# Create and plot the NACA 0012 airfoil
naca0012_airfoil = asb.Airfoil("naca0012")
plt.figure(figsize=(12, 4))
naca0012_airfoil.draw()
plt.title("NACA 0012 Airfoil")
plt.xlabel("x/c")
plt.ylabel("y/c")
plt.grid(True)
plt.axis('equal')
plt.show()