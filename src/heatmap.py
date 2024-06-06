import numpy as np
import matplotlib.pyplot as plt
from netCDF4 import Dataset

file_path = '/Users/arpitasen/Desktop/Sanghavi/Data/EMIT_L1B_RAD_001_20231026T175210_2329912_009.nc'  # Replace with the correct file path
nc = Dataset(file_path, mode='r')
radiance = nc.variables['radiance'][:]

start_wavelength = 381  # in nm
end_wavelength = 2493  # in nm
num_bands = 285
band_indices = np.arange(num_bands)
wavelengths = start_wavelength + (end_wavelength - start_wavelength) / (num_bands - 1) * band_indices

radiance_selected_bands = radiance[500, 500, 202:229]  # Bands 48 to 54 are indexed as 47 to 53
wavelengths_selected_bands = wavelengths[202:229]

plt.figure(figsize=(12, 8)) 
plt.plot(wavelengths_selected_bands, radiance_selected_bands, linewidth=2, markersize=5, linestyle='-', color='b')
plt.xlabel('Wavelength (nm)', fontsize=14, fontweight='bold', color='darkblue')
plt.ylabel('Radiance', fontsize=14, fontweight='bold', color='darkblue')
plt.title('Absorption Spectrum CO2', fontsize=16, fontweight='bold', color='red')
plt.grid(True, which='both', linestyle='--', linewidth=0.5)
plt.minorticks_on()
plt.legend(['Radiance'], loc='best', fontsize=12)
plt.tick_params(axis='both', which='major', labelsize=12, direction='in', length=6, width=2)
plt.tick_params(axis='both', which='minor', labelsize=10, direction='in', length=3, width=1)
plt.show()