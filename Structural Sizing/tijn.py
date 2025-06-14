from scipy.integrate import quad

# Define the lift distribution function: L(z) = 111.11 * z^2
def lift_distribution(z):
    return 111.11 * z**2

# Centroid and total lift computation function
def Compute_Total_Lift_and_Centroid(Y_func, a, b):
    total_lift, _ = quad(Y_func, a, b)
    moment, _ = quad(lambda x: x * Y_func(x), a, b)
    x_centroid = moment / total_lift 
    return total_lift, x_centroid

# Inputs
a = 0         # start of the beam (root)
b = 1.5       # end of the beam (tip)

# Run the calculation
lift, centroid = Compute_Total_Lift_and_Centroid(lift_distribution, a, b)

# Output the results
print(f"Total lift: {lift:.3f} N")
print(f"Centroid location: {centroid:.4f} m")
