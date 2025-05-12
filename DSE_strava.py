import gpxpy

# Load the GPX file
with open('Lunch_Run.gpx', 'r') as gpx_file:
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
                point.latitude,        # Latitude
                point.longitude,       # Longitude
                point.elevation  ]      # Elevation
            )


print(bike_data) #time since start (s), latitude, longitude, elevation