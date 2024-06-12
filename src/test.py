import numpy as np
from netCDF4 import Dataset

# Define the file path
file_path = "/Users/arpitasen/Desktop/Sanghavi/Data/EMIT_L1B_RAD_001_20231026T175210_2329912_009.nc"

# Open the NetCDF file and read the radiance data
ds = Dataset(file_path, "r")
radiance = ds.variables["radiance"][:]
ds.close()

# Select the band index and normalize it
band_index = 52 
selected_band = radiance[band_index, :, :]

# Define the output file path
output_file_path = "/Users/arpitasen/Desktop/Sanghavi/Data/normalized_radiance_band_52.txt"

# Save the normalized data to a text file
np.savetxt(output_file_path, selected_band)

print(f"Normalized radiance data saved to {output_file_path}")

