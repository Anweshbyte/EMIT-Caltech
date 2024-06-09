import numpy as np
from netCDF4 import Dataset

def calculate_radiance_depth(file_path, pixel_x, pixel_y, start_band, end_band):
    nc = Dataset(file_path, mode='r')
    radiance = nc.variables['radiance'][:]
    start_wavelength = 381  # in nm
    end_wavelength = 2493  # in nm
    num_bands = 285
    
    band_indices = np.arange(num_bands)
    wavelengths = start_wavelength + (end_wavelength - start_wavelength) / (num_bands - 1) * band_indices
    
    radiance_selected_bands = radiance[pixel_x, pixel_y, start_band:end_band]
    wavelengths_selected_bands = wavelengths[start_band:end_band]
    
    num_selected_bands = end_band - start_band
    bands_per_group = 5
    num_groups = num_selected_bands // bands_per_group
    radiance_bands = radiance_selected_bands[:num_groups * bands_per_group].reshape(num_groups, bands_per_group)
    
    radiance_depth = np.zeros_like(radiance_selected_bands)
    for band in radiance_bands:
        highest_values = np.sort(band)[-2:]  
        for i, value in enumerate(band):
            radiance_depth[5 * np.where(radiance_bands == band)[0][0] + i] = value / np.mean(highest_values)
    nc.close()
    
    return wavelengths_selected_bands, radiance_depth



# import numpy as np
# import matplotlib.pyplot as plt
# from netCDF4 import Dataset

# file_path = '/Users/arpitasen/Desktop/Sanghavi/Data/EMIT_L1B_RAD_001_20231026T175210_2329912_009.nc'  # Replace with the correct file path
# nc = Dataset(file_path, mode='r')
# radiance = nc.variables['radiance'][:]

# start_wavelength = 381  # in nm
# end_wavelength = 2493  # in nm
# num_bands = 285
# band_indices = np.arange(num_bands)
# wavelengths = start_wavelength + (end_wavelength - start_wavelength) / (num_bands - 1) * band_indices

# radiance_selected_bands = radiance[500, 500, 48:58]  # Bands 48 to 54 are indexed as 47 to 53
# wavelengths_selected_bands = wavelengths[48:58]

# # Reshape radiance values into bands of 5
# radiance_bands = radiance_selected_bands.reshape(-1, 5)

# # Calculate depth of radiance values in each band
# radiance_depth = np.zeros_like(radiance_selected_bands)
# for band in radiance_bands:
#     # Find the two highest values in the band
#     highest_values = np.sort(band)[-2:]
#     for i, value in enumerate(band):
#         # Calculate depth for each value in the band
#         radiance_depth[5 * np.where(radiance_bands == band)[0][0] + i] = value / np.mean(highest_values)

# plt.figure(figsize=(12, 8))
# plt.plot(wavelengths_selected_bands, radiance_depth, linewidth=2, markersize=5, linestyle='-', color='b')
# plt.xlabel('Wavelength (nm)', fontsize=14, fontweight='bold', color='darkblue')
# plt.ylabel('Depth of Radiance', fontsize=14, fontweight='bold', color='darkblue')
# plt.title('Depth of Radiance', fontsize=16, fontweight='bold', color='red')
# plt.grid(True, which='both', linestyle='--', linewidth=0.5)
# plt.minorticks_on()
# plt.legend(['Depth of Radiance'], loc='best', fontsize=12)
# plt.tick_params(axis='both', which='major', labelsize=12, direction='in', length=6, width=2)
# plt.tick_params(axis='both', which='minor', labelsize=10, direction='in', length=3, width=1)
# plt.show()




# import numpy as np
# import matplotlib.pyplot as plt
# from netCDF4 import Dataset

# file_path = '/Users/arpitasen/Desktop/Sanghavi/Data/EMIT_L1B_RAD_001_20231026T175210_2329912_009.nc'  # Replace with the correct file path
# nc = Dataset(file_path, mode='r')
# radiance = nc.variables['radiance'][:]

# start_wavelength = 381  # in nm
# end_wavelength = 2493  # in nm
# num_bands = 285
# band_indices = np.arange(num_bands)
# wavelengths = start_wavelength + (end_wavelength - start_wavelength) / (num_bands - 1) * band_indices

# radiance_selected_bands = radiance[500, 500, 48:55]  # Bands 48 to 54 are indexed as 47 to 53
# wavelengths_selected_bands = wavelengths[48:55]

# plt.figure(figsize=(12, 8)) 
# plt.plot(wavelengths_selected_bands, radiance_selected_bands, linewidth=2, markersize=5, linestyle='-', color='b')
# plt.xlabel('Wavelength (nm)', fontsize=14, fontweight='bold', color='darkblue')
# plt.ylabel('Radiance', fontsize=14, fontweight='bold', color='darkblue')
# plt.title('Absorption Spectrum CO2', fontsize=16, fontweight='bold', color='red')
# plt.grid(True, which='both', linestyle='--', linewidth=0.5)
# plt.minorticks_on()
# plt.legend(['Radiance'], loc='best', fontsize=12)
# plt.tick_params(axis='both', which='major', labelsize=12, direction='in', length=6, width=2)
# plt.tick_params(axis='both', which='minor', labelsize=10, direction='in', length=3, width=1)
# plt.show()

# import numpy as np
# import matplotlib.pyplot as plt
# from netCDF4 import Dataset

# file_path = '/Users/arpitasen/Desktop/Sanghavi/Data/EMIT_L1B_RAD_001_20231026T175210_2329912_009.nc'  # Replace with the correct file path
# nc = Dataset(file_path, mode='r')
# radiance = nc.variables['radiance'][:]

# start_wavelength = 381  # in nm
# end_wavelength = 2493  # in nm
# num_bands = 285
# band_indices = np.arange(num_bands)
# wavelengths = start_wavelength + (end_wavelength - start_wavelength) / (num_bands - 1) * band_indices

# radiance_selected_bands = radiance[500, 500, 48:53]  # Bands 48 to 54 are indexed as 47 to 53
# wavelengths_selected_bands = wavelengths[48:53]

# radiance_depth = np.zeros_like(radiance_selected_bands)
# for i in range(len(radiance_selected_bands)):
#     if i == 0 or i == len(radiance_selected_bands) - 1:
#         radiance_depth[i] = 0
#     else:
#         radiance_depth[i] = np.abs(radiance_selected_bands[i]/(radiance_selected_bands[i-1] + radiance_selected_bands[i+1]) / 2)

# plt.figure(figsize=(12, 8)) 
# plt.plot(wavelengths_selected_bands, radiance_depth, linewidth=2, markersize=5, linestyle='-', color='b')
# plt.xlabel('Wavelength (nm)', fontsize=14, fontweight='bold', color='darkblue')
# plt.ylabel('Depth of Radiance', fontsize=14, fontweight='bold', color='darkblue')
# plt.title('Depth of Radiance', fontsize=16, fontweight='bold', color='red')
# plt.grid(True, which='both', linestyle='--', linewidth=0.5)
# plt.minorticks_on()
# plt.legend(['Depth of Radiance'], loc='best', fontsize=12)
# plt.tick_params(axis='both', which='major', labelsize=12, direction='in', length=6, width=2)
# plt.tick_params(axis='both', which='minor', labelsize=10, direction='in', length=3, width=1)
# plt.show()