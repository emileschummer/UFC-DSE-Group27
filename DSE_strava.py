import gpxpy

# Load the GPX file
with open('Lunch_Run.gpx', 'r') as gpx_file:
    gpx = gpxpy.parse(gpx_file)

# Extract data
for track in gpx.tracks:
    for segment in track.segments:
        for point in segment.points:
            print(f"Time: {point.time}, Latitude: {point.latitude}, Longitude: {point.longitude}, Elevation: {point.elevation}")