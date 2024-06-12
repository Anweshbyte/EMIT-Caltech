using NCDatasets
using LinearAlgebra
using Plots
using Statistics
using Missings

file_path = "/Users/arpitasen/Desktop/Sanghavi/Data/EMIT_L1B_RAD_001_20231222T191915_2335613_007.nc"
ds = Dataset(file_path, "r")
radiance = ds["radiance"][:]
lon = ds.group["location"]["lon"][:]
lat = ds.group["location"]["lat"][:]
close(ds)

band_index = 52
selected_band = radiance[band_index, :, :]
filtered_band = skipmissing(selected_band)
min_value = minimum(filtered_band)
max_value = maximum(filtered_band)
normalized_band = (selected_band .- min_value) ./ (max_value - min_value)

target_lat_lon = [34.0, -118.25]
distances = sqrt.((lat .- target_lat_lon[1]).^2 + (lon .- target_lat_lon[2]).^2)
closest_index = argmin(distances)
println(closest_index)

# heatmap(normalized_band, aspect_ratio=:equal, color=:viridis, xlabel="Longitude", ylabel="Latitude", title="Normalized Heatmap with Closest Point")
# scatter!([closest_index[2]], [closest_index[1]], color=:red, marker=:dot, markersize=5, label="Closest Point")













