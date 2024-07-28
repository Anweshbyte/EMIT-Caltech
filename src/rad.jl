using NCDatasets
using Plots
using AWSS3

function band_to_wavelength(band_number::Int)
    min_wavelength = 381
    max_wavelength = 2493
    total_bands = 285
    wavelength_range = max_wavelength - min_wavelength
    wavelength_per_band = wavelength_range / total_bands
    wavelength = min_wavelength + (band_number - 1) * wavelength_per_band
    return wavelength
end

file_paths = [
    "/Users/arpitasen/Desktop/Sanghavi/Data/EMIT_L1B_RAD_001_20230430T164419_2312011_002.nc",
    "/Users/arpitasen/Desktop/Sanghavi/Data/EMIT_L1B_RAD_001_20230614T224902_2316515_008.nc",
    "/Users/arpitasen/Desktop/Sanghavi/Data/EMIT_L1B_RAD_001_20230728T214106_2320914_002.nc",
    "/Users/arpitasen/Desktop/Sanghavi/Data/EMIT_L1B_RAD_001_20231022T192739_2329513_007.nc",
    "/Users/arpitasen/Desktop/Sanghavi/Data/EMIT_L1B_RAD_001_20231026T175222_2329912_010.nc",
    "/Users/arpitasen/Desktop/Sanghavi/Data/EMIT_L1B_RAD_001_20231222T191915_2335613_007.nc",
]

pixel_x = 1050
pixel_y = 500
band_start = 49
band_end = 54
bands = band_start:band_end

file_dates = [match(r"(\d{8})", file_path).match for file_path in file_paths]
plot()

for (i, file_path) in enumerate(file_paths)
    ds = Dataset(file_path, "r")
    radiance = ds["radiance"][:]
    radiance_values = radiance[band_start:band_end, pixel_x, pixel_y]
    close(ds)
    band_numbers = band_start:band_end
    wavelengths = map(band_to_wavelength, band_numbers)
    file_date = file_dates[i]
    plot!(wavelengths, radiance_values, label="$file_date", marker=:o)
end

xlabel!("Band")
ylabel!("Radiance")
title!("Radiance")
savefig("/Users/arpitasen/Desktop/Sanghavi/Data/rad.png")