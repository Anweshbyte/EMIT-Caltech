import os
import matplotlib.pyplot as plt
from linedep import calculate_radiance_depth

file_path = '/Users/arpitasen/Desktop/Sanghavi/Data/EMIT_L1B_RAD_001_20231026T175210_2329912_009.nc'
start_band = 48
end_band = 58

xy_coordinates = [
    (1058, 453),
    (1184, 860),
    (621, 1010)
]

colors = ['y', 'g', 'r']  # Updated colors

plt.figure(figsize=(12, 8))

for idx, (pixel_x, pixel_y) in enumerate(xy_coordinates):
    wavelengths_selected_bands, radiance_depth = calculate_radiance_depth(file_path, pixel_x, pixel_y, start_band, end_band)
    plt.plot(wavelengths_selected_bands, radiance_depth, linewidth=2, markersize=5, linestyle='-', color=colors[idx % len(colors)])

plt.xlabel('Wavelength (nm)', fontsize=14, fontweight='bold', color='darkblue')
plt.ylabel('Depth of Radiance', fontsize=14, fontweight='bold', color='darkblue')
plt.title('Depth of Radiance', fontsize=16, fontweight='bold', color='red')
plt.grid(True, which='both', linestyle='--', linewidth=0.5)
plt.minorticks_on()
plt.legend(loc='best', fontsize=12)
plt.tick_params(axis='both', which='major', labelsize=12, direction='in', length=6, width=2)
plt.tick_params(axis='both', which='minor', labelsize=10, direction='in', length=3, width=1)
plt.show()
