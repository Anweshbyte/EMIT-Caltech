import numpy as np
import matplotlib.pyplot as plt
from netCDF4 import Dataset
from matplotlib.patches import FancyArrow

file_path = '/Users/arpitasen/Desktop/Sanghavi/Data/EMIT_L1B_RAD_001_20231026T175210_2329912_009.nc'  # Replace with the correct file path
nc = Dataset(file_path, mode='r')
radiance = nc.variables['radiance'][:]

start_band = 48
end_band = 53
reflectance_selected_bands = radiance[:, :, start_band:end_band]
reflectance_selected_bands = reflectance_selected_bands[:, :, 4]
normalized_data = reflectance_selected_bands / np.max(reflectance_selected_bands)

lat_tl, lon_tl =  34.8782616, -118.9883423
lat_tr, lon_tr =  34.3296089, -118.2988434 
lat_bl, lon_bl =  34.2534752, -119.4855042
lat_br, lon_br =  33.7048225, -118.7960052 

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

# Add a north arrow
# arrow_length = 0.05 * image_height  # Length of the arrow
# north_lat, north_lon = transform_pixel_to_geo(image_width, 0)
# north_x, north_y = transform_geo_to_pixel(north_lat, north_lon)

# plt.gca().add_patch(FancyArrow(image_width - arrow_length, arrow_length, 
#                                -0.8 * arrow_length, 0.8 * arrow_length, 
#                                width=0.02 * image_height, head_width=0.05 * image_height, 
#                                head_length=0.05 * image_height, fc='white', ec='white'))

plt.show()

# plt.figure(figsize=(10, 8))
# plt.imshow(normalized_data, cmap='viridis')
# plt.colorbar(label='Normalized Reflectance')
# plt.title(f'Normalized Radiance Heat Map')
# plt.xlabel('Pixel X')
# plt.ylabel('Pixel Y')
# plt.show()

