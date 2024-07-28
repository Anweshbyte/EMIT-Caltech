# Load data from the YAML configuration file
geos_data = loadGeos("GeosChem.yml")

# Access data using internal variable names
ch4 = geos_data.data["ch4"]
latitude = geos_data.data["lat"]