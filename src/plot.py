import numpy as np
import matplotlib.pyplot as plt
from netCDF4 import Dataset

file_path = '/Users/arpitasen/Desktop/Sanghavi/Data/EMIT_L1B_RAD_001_20231026T175210_2329912_009.nc'  # Replace with the correct file path
nc = Dataset(file_path, mode='r')
radiance = nc.variables['radiance'][:]

start_band = 48
end_band = 53
reflectance_selected_bands = radiance[:, :, start_band:end_band]
reflectance_selected_bands = reflectance_selected_bands[:, :, 2]
normalized_data = reflectance_selected_bands / np.max(reflectance_selected_bands)
# np.savetxt('normalized_data.txt', reflectance_selected_bands)

plt.figure(figsize=(10, 8))
plt.imshow(normalized_data, cmap='viridis')
plt.colorbar(label='Normalized Reflectance')
plt.title(f'Radiance Heat Map for Bands {start_band} to {end_band - 1}')
plt.xlabel('Pixel X')
plt.ylabel('Pixel Y')
plt.show()

