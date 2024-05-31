import netCDF4
import numpy as np
import matplotlib.pyplot as plt
from netCDF4 import Dataset


jan = Dataset('/Users/arpitasen/Desktop/Sanghavi/Data/EMIT_L1B_RAD_001_20231026T175210_2329912_009.nc')
print(jan.variables.keys()) # Prints the dictionary keys of available measurement types

reflectance = jan.variables['radiance']
start_band = 50 # Oxy - A Band
end_band = 51 # Oxy - A Band

reflectance_selected_bands = reflectance[:, :, start_band:end_band]
print(f"Shape of reflectance data for bands {start_band} to {end_band - 1}: {reflectance_selected_bands.shape}")
reflectance_selected_bands = reflectance_selected_bands[:, :, 0]
normalized_data = reflectance_selected_bands / np.max(reflectance_selected_bands)

plt.figure(figsize=(10, 8))
plt.imshow(normalized_data, cmap='viridis')
plt.colorbar(label='Normalized Reflectance')
plt.title(f'Reflectance Heat Map for Bands {start_band} to {end_band - 1}')
plt.xlabel('Pixel X')
plt.ylabel('Pixel Y')
plt.show()

