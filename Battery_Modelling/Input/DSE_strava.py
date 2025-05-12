




import gpxpy
import numpy as np
# Load the GPX file
with open('C:\\Users\\tijnp\\OneDrive\\Documenten\\Phyton\\DSE\\UFC-DSE-Group27\\Battery_Modelling\\Input\\Lunch_Run.gpx', 'r') as gpx_file:
    gpx = gpxpy.parse(gpx_file)
bike_data = []
# Extract data
for track in gpx.tracks:
    for segment in track.segments:
        points = segment.points
        if not points:
            continue
        
        # Get reference start time
        start_time = points[0].time

        for point in points:
            time_delta = (point.time - start_time).total_seconds()  # Time difference in seconds
            bike_data.append([
                time_delta,            # Time since start in seconds
                point.latitude*np.pi/180,        # Latitude
                point.longitude*np.pi/180,       # Longitude
                point.elevation  ]      # Elevation
            )
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




 #time since start (s), latitude, longitude, elevation
time_data = []
velocity_data = []
incline_data = []
density_data = []
R = 6378000 #radius earth in meter
for i in range(len(bike_data)):
    if i >0:
        t1 = bike_data[i-1][0]
        t2 = bike_data[i][0]
        altitude1 = bike_data[i-1][3]
        altitude2 = bike_data[i][3]
        latitude1 = bike_data[i-1][1]
        latitude2 = bike_data[i][1]
        longitude1 = bike_data[i-1][2]
        longitude2 = bike_data[i][2] 
        delta_latitude = latitude2 - latitude1
        delta_longitude = longitude2 - longitude1
        distance = 2*R*np.arcsin((np.sin(delta_latitude/2)**2+np.cos(latitude1)*np.sin(latitude2)*np.sin(delta_longitude)**2)**0.5)
        velocity = distance/(t2 - t1)
        incline = np.arctan((altitude2 - altitude1)/distance)
        rho = air_density_isa(altitude2)
        time_data.append(t2)
        velocity_data.append(velocity)
        incline_data.append(incline)  
        density_data.append(rho)

import matplotlib.pyplot as plt
plt.plot(time_data,velocity_data)
plt.plot(time_data,incline_data)
plt.plot(time_data,density_data)
plt.show()