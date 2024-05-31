import netCDF4
from netCDF4 import Dataset

# Load the NetCDF file
jan = Dataset('/Users/arpitasen/Desktop/Sanghavi/Data/EMIT_L2A_RFL_001_20220903T163129_2224611_012.nc')
reflectance = jan.variables['reflectance']
start_band = 50
end_band = 54  # Since slicing in Python is end-exclusive, we use 54 to include band 53
reflectance_selected_bands = reflectance[:, :, start_band:end_band]
print(f"Shape of reflectance data for bands {start_band} to {end_band - 1}: {reflectance_selected_bands.shape}")
print(reflectance_selected_bands)

