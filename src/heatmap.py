import numpy as np
import matplotlib.pyplot as plt
from netCDF4 import Dataset

# Load the data
file_path = '/Users/arpitasen/Desktop/Sanghavi/Data/EMIT_L1B_RAD_001_20231022T192727_2329513_006.nc'  # Replace with the correct file path
nc = Dataset(file_path, mode='r')
radiance = nc.variables['radiance'][:]

# Select the bands and normalize the data
start_band = 48
end_band = 53
reflectance_selected_bands = radiance[:, :, start_band:end_band]
reflectance_selected_bands = reflectance_selected_bands[:, :, 4]
normalized_data = reflectance_selected_bands / np.max(reflectance_selected_bands)

# Define the corner coordinates
lat_tl, lon_tl = 34.8782616, -118.9883423
lat_tr, lon_tr = 34.3296089, -118.2988434 
lat_bl, lon_bl = 34.2534752, -119.4855042
lat_br, lon_br = 33.7048225, -118.7960052 

# Define the pixel dimensions of the image
image_height, image_width = normalized_data.shape

# Compute transformation coefficients (simple linear assumption)
def transform_pixel_to_geo(x, y):
    lat = lat_tl + (lat_bl - lat_tl) * (y / image_height) + (lat_tr - lat_tl) * (x / image_width)
    lon = lon_tl + (lon_br - lon_tl) * (y / image_height) + (lon_tr - lon_tl) * (x / image_width)
    return lat, lon

# Compute inverse transformation for placing geo-referenced elements
def transform_geo_to_pixel(lat, lon):
    a = (lat_tl - lat_bl) / image_height
    b = (lat_tr - lat_tl) / image_width
    c = lat_tl
    d = (lon_tl - lon_bl) / image_height
    e = (lon_tr - lon_tl) / image_width
    f = lon_tl

    y = (lat - c - b * (lon - f) / e) / (a - b * d / e)
    x = (lon - f - d * y) / e
    return x, y

# Find the coordinates of the highest, value close to 0.2, and intermediate radiance values
highest_radiance_coords = np.unravel_index(np.argmax(normalized_data), normalized_data.shape)
lowest_radiance_coords = np.unravel_index(np.argmin(normalized_data), normalized_data.shape)

# Find the coordinates closest to a radiance value of 0.2
value_0_2_coords = np.unravel_index(np.argmin(np.abs(normalized_data - 0.21)), normalized_data.shape)

# Calculate the median radiance value and find the nearest coordinate
median_radiance_value = np.median(normalized_data)
median_radiance_coords = np.unravel_index(np.argmin(np.abs(normalized_data - median_radiance_value)), normalized_data.shape)

# Print the radiance values with their coordinates
highest_radiance_value = normalized_data[highest_radiance_coords]
value_0_2_radiance_value = normalized_data[value_0_2_coords]
median_radiance_value = normalized_data[median_radiance_coords]

print(f'Highest Radiance Value: {highest_radiance_value}, Coordinates: {highest_radiance_coords}')
print(f'Radiance Value close to 0.2: {value_0_2_radiance_value}, Coordinates: {value_0_2_coords}')
print(f'Median Radiance Value: {median_radiance_value}, Coordinates: {median_radiance_coords}')

# Plot the image
plt.figure(figsize=(10, 8))
plt.imshow(normalized_data, cmap='viridis')
plt.colorbar(label='Normalized Reflectance')

# Add latitude and longitude labels
num_labels = 5  # Number of labels to display along each axis
x_labels = np.linspace(0, image_width, num_labels)
y_labels = np.linspace(0, image_height, num_labels)

# Compute and set x and y tick labels
x_tick_labels = [f'{transform_pixel_to_geo(x, 0)[1]:.2f}' for x in x_labels]
y_tick_labels = [f'{transform_pixel_to_geo(0, y)[0]:.2f}' for y in y_labels]

plt.xticks(x_labels, x_tick_labels)
plt.yticks(y_labels, y_tick_labels)

plt.title('Normalized Radiance Heat Map')
plt.xlabel('Longitude')
plt.ylabel('Latitude')

# Add circles for highest, value close to 0.2, and median radiance values
circle_high = plt.Circle((highest_radiance_coords[::-1]), radius=20, color='red', fill=False, linewidth=2, label='Cloudy')
circle_0_2 = plt.Circle((value_0_2_coords[::-1]), radius=20, color='yellow', fill=False, linewidth=2, label='Clear')
circle_median = plt.Circle((median_radiance_coords[::-1]), radius=20, color='green', fill=False, linewidth=2, label='Mean (Haze)')

ax = plt.gca()
ax.add_patch(circle_high)
ax.add_patch(circle_0_2)
ax.add_patch(circle_median)

plt.legend()
plt.show()
