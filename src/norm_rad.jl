using Plots
using NCDatasets
using Statistics

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
start_band = 49
end_band = 55

function normalize_radiance(radiance)
    num_bands = size(radiance, 1)
    normalized_radiance = similar(radiance)

    for i in 1:5:num_bands
        group_end = min(i + 4, num_bands)
        group = radiance[i:group_end, pixel_x, pixel_y]
        top2max = sort(group, rev=true)[1:2]
        group_norm = group ./ mean(top2max)
        normalized_radiance[i:group_end, pixel_x, pixel_y] .= group_norm
    end

    return normalized_radiance
end

normalized_radiance_data = []

for file_path in file_paths
    dataset = Dataset(file_path, "r")
    radiance = dataset["radiance"][:, :, :]
    normalized_radiance = normalize_radiance(radiance)
    push!(normalized_radiance_data, normalized_radiance)
    close(dataset)
end

plot()

bands_to_plot = start_band:end_band

for (i, normalized_radiance) in enumerate(normalized_radiance_data)
    plot!(bands_to_plot, normalized_radiance[bands_to_plot, pixel_x, pixel_y],
          label="File $i",)
end

xlabel!("Band Index")
ylabel!("Normalized Radiance")
title!("Normalized Radiance at Pixel ($pixel_x, $pixel_y)")
display(plot)
savefig("/Users/arpitasen/Desktop/Sanghavi/Data/norm_rad.png")
