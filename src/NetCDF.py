import netCDF4
from netCDF4 import Dataset


jan = Dataset('/Users/arpitasen/Desktop/Sanghavi/Data/EMIT_L1B_RAD_001_20240423T183357_2411412_006.nc')
print(jan.variables.keys()) # Prints the dictionary keys of available measurement types

reflectance = jan.variables['radiance']
start_band = 50 # Oxy - A Band
end_band = 51 # Oxy - A Band

reflectance_selected_bands = reflectance[:, :, start_band:end_band]
print(f"Shape of reflectance data for bands {start_band} to {end_band - 1}: {reflectance_selected_bands.shape}")
print(reflectance_selected_bands)

