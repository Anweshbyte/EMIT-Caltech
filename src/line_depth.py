import numpy as np
import matplotlib.pyplot as plt
from netCDF4 import Dataset
from scipy.ndimage import convolve

file_path = '/Users/arpitasen/Desktop/Sanghavi/Data/EMIT_L1B_RAD_001_20231026T175210_2329912_009.nc'
nc = Dataset(file_path, mode='r')
radiance = nc.variables['radiance'][:]

start_band = 48
end_band = 53
reflectance_selected_bands = radiance[:, :, start_band:end_band]
normalized_data = reflectance_selected_bands / np.max(reflectance_selected_bands, axis=(0, 1))

def calculate_line_depth(data):
    kernel = np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]]) / 8.0
    neighbors_avg = convolve(data, kernel, mode='constant', cval=0.0)
    line_depth = np.divide(data, neighbors_avg, out=np.zeros_like(data), where=neighbors_avg!=0)
    return line_depth

line_depths = [calculate_line_depth(normalized_data[:, :, i]) for i in range(normalized_data.shape[2])]
num_bands = normalized_data.shape[2]
fig, axes = plt.subplots(1, num_bands, figsize=(20, 8))

max_line_depth = np.max([np.max(line_depth) for line_depth in line_depths])
min_line_depth = np.min([np.min(line_depth) for line_depth in line_depths])
print(f"Maximum Line Depth: {max_line_depth}")
print(f"Minimum Line Depth: {min_line_depth}")

for band_index in range(num_bands):
    ax = axes[band_index]
    im = ax.imshow(line_depths[band_index], cmap='viridis', vmin=0.5, vmax=1.0)
    ax.set_title(f'Band {start_band + band_index}')
    ax.set_xlabel('Pixel X')
    ax.set_ylabel('Pixel Y')
    fig.colorbar(im, ax=ax, orientation='vertical', label='Line Depth')

plt.tight_layout()
plt.show()
