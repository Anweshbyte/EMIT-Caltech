import numpy as np
import matplotlib.pyplot as plt
from netCDF4 import Dataset

file_path = '/Users/arpitasen/Desktop/Sanghavi/Data/EMIT_L1B_RAD_001_20231026T175210_2329912_009.nc'  # Replace with the correct file path
nc = Dataset(file_path, mode='r')
radiance = nc.variables['radiance'][:]

start_band = 48
end_band = 53
reflectance_selected_bands = radiance[:, :, start_band:end_band]
reflectance_selected_bands = reflectance_selected_bands[:, :, 4]
normalized_data = reflectance_selected_bands / np.max(reflectance_selected_bands)

lat_tl, lon_tl =  34.8782616, -118.9883423
lat_tr, lon_tr =  34.2534752, -119.4855042
lat_bl, lon_bl =  33.7048225, -118.7960052 
lat_br, lon_br =  34.3296089, -118.2988434

image_height, image_width = normalized_data.shape

def interpolate_lat(y):
    return lat_tl + (lat_bl - lat_tl) * (y / image_height)

def interpolate_lon(x):
    return lon_tl + (lon_tr - lon_tl) * (x / image_width)

x_coords = np.linspace(0, image_width, image_width)
y_coords = np.linspace(0, image_height, image_height)
latitudes = np.array([interpolate_lat(y) for y in y_coords])
longitudes = np.array([interpolate_lon(x) for x in x_coords])

plt.figure(figsize=(10, 8))
plt.imshow(normalized_data, cmap='viridis')
plt.colorbar(label='Normalized Reflectance')
num_labels = 5  # Number of labels to display along each axis
x_labels = np.linspace(0, image_width, num_labels)
y_labels = np.linspace(0, image_height, num_labels)
x_tick_labels = [f'{interpolate_lon(x):.2f}' for x in x_labels]
y_tick_labels = [f'{interpolate_lat(y):.2f}' for y in y_labels]
plt.xticks(x_labels, x_tick_labels)
plt.yticks(y_labels, y_tick_labels)
plt.title('Normalized Radiance Heat Map')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.show()

# plt.figure(figsize=(10, 8))
# plt.imshow(normalized_data, cmap='viridis')
# plt.colorbar(label='Normalized Reflectance')
# plt.title(f'Normalized Radiance Heat Map')
# plt.xlabel('Pixel X')
# plt.ylabel('Pixel Y')
# plt.show()

