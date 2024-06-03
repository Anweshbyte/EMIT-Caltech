import numpy as np
import matplotlib.pyplot as plt
from netCDF4 import Dataset

file_path = '/Users/arpitasen/Desktop/Sanghavi/Data/EMIT_L1B_RAD_001_20231026T175210_2329912_009.nc'  # Replace with the correct file path
nc = Dataset(file_path, mode='r')
radiance = nc.variables['radiance'][:]

# start_wavelength = 381  # in nm
# end_wavelength = 2493  # in nm
# num_bands = 285
# band_indices = np.arange(num_bands)
# wavelengths = start_wavelength + (end_wavelength - start_wavelength) / (num_bands - 1) * band_indices

# radiance_selected_bands = radiance[500, 500, 270:285]  # Bands 48 to 54 are indexed as 47 to 53
# wavelengths_selected_bands = wavelengths[270:285]

# plt.figure(figsize=(10, 6))
# plt.plot(wavelengths_selected_bands, radiance_selected_bands, marker='o')
# plt.xlabel('Wavelength (nm)')
# plt.ylabel('Radiance')
# plt.title('Radiance Values for Wavelengths 48 to 54 at Point (500, 500)')
# plt.grid(True)
# plt.show()
# nc.close()

start_band = 48
end_band = 53
reflectance_selected_bands = radiance[:, :, start_band:end_band]
print(f"Shape of reflectance data for bands {start_band} to {end_band - 1}: {reflectance_selected_bands.shape}")
reflectance_selected_bands = reflectance_selected_bands[:, :, 0]
normalized_data = reflectance_selected_bands / np.max(reflectance_selected_bands)

plt.figure(figsize=(10, 8))
plt.imshow(normalized_data, cmap='viridis')
plt.colorbar(label='Normalized Reflectance')
plt.title(f'Radiance Heat Map for Bands {start_band} to {end_band - 1}')
plt.xlabel('Pixel X')
plt.ylabel('Pixel Y')
plt.show()

