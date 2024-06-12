include("utils.jl")

file_paths = [
    "/Users/arpitasen/Desktop/Sanghavi/Data/EMIT_L1B_RAD_001_20230430T164419_2312011_002.nc",
    "/Users/arpitasen/Desktop/Sanghavi/Data/EMIT_L1B_RAD_001_20230614T224902_2316515_008.nc",
    "/Users/arpitasen/Desktop/Sanghavi/Data/EMIT_L1B_RAD_001_20230728T214106_2320914_002.nc",
    "/Users/arpitasen/Desktop/Sanghavi/Data/EMIT_L1B_RAD_001_20231022T192739_2329513_007.nc",
    "/Users/arpitasen/Desktop/Sanghavi/Data/EMIT_L1B_RAD_001_20231026T175222_2329912_010.nc",
    "/Users/arpitasen/Desktop/Sanghavi/Data/EMIT_L1B_RAD_001_20231222T191915_2335613_007.nc",
]

pixel_x = 1057
pixel_y = 513
start_band = 45
end_band = 54

plot_normalized_radiance_multiple(file_paths, pixel_x, pixel_y, start_band, end_band)


