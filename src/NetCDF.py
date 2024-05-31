import netCDF4
from netCDF4 import Dataset

jan = Dataset('/Users/arpitasen/Desktop/Sanghavi/Data/EMIT_L2A_RFL_001_20220903T163129_2224611_012.nc')
reflectance = jan.variables['reflectance']
shape = reflectance.shape
print("Shape of reflectance variable:", shape)
num_bands = shape[2]
print("Number of bands:", num_bands)

print(f"Reflectance data type: {reflectance.dtype}")
print(f"Reflectance dimensions: {reflectance.dimensions}")

band_index = 0
reflectance_band = reflectance[:, :, band_index]
print(f"Reflectance data for band {band_index}:")
print(reflectance_band)

for band in range(num_bands):
    reflectance_band = reflectance[:, :, band]
    print(f"Reflectance data for band {band}:")
    print(reflectance_band)
