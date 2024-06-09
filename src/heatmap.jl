using NCDatasets
using Plots
using StatsBase

file_path = "/Users/arpitasen/Desktop/Sanghavi/Data/EMIT_L1B_RAD_001_20231022T192727_2329513_006.nc"
ds = Dataset(file_path, "r")
radiance = ds["radiance"][:]
close(ds)
band_index = 100  # Change this to the desired band index
selected_band = radiance[band_index, :, :]
normalized_band = (selected_band .- minimum(selected_band)) ./ (maximum(selected_band) - minimum(selected_band))
heatmap(normalized_band, color=:viridis, title="Normalized Heatmap of Band $band_index", xlabel="Pixel X", ylabel="Pixel Y")
display(heatmap(normalized_band, color=:viridis, title="Normalized Heatmap of Band $band_index", xlabel="Pixel X", ylabel="Pixel Y"))
