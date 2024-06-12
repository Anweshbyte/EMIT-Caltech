using NCDatasets
using Plots
using LinearAlgebra
using Statistics
using Missings

file_path = "/Users/arpitasen/Desktop/Sanghavi/Data/EMIT_L1B_RAD_001_20231026T175210_2329912_009.nc"
ds = Dataset(file_path, "r")
radiance = ds["radiance"][:]
close(ds)

band_index = 52
selected_band = radiance[band_index, :, :]

filtered_band = skipmissing(selected_band)
min_value = minimum(filtered_band)
max_value = maximum(filtered_band)
normalized_band = (selected_band .- min_value) ./ (max_value - min_value)

#[TL BL BR TR]
corner_coords = [
    [-118.6199951 34.9586945],  # top-left
    [-119.11763 34.3332062],  # bottom-left
    [-118.426239 33.7831345],  # bottom-right
    [-117.9286041 34.4086227]   # top-right
]

n_rows, n_cols = size(normalized_band)
lon_min, lat_min = corner_coords[2][1], corner_coords[2][2]
lon_max, lat_max = corner_coords[3][1], corner_coords[1][2]

lon_per_pixel = abs((lon_max - lon_min) / n_cols)
lat_per_pixel = abs((lat_max - lat_min) / n_rows)

function point_to_line_distance(line_point1, line_point2, point)
    line_vec = line_point2 .- line_point1
    point_vec = point .- line_point1
    proj = (dot(point_vec, line_vec) / dot(line_vec, line_vec)) * line_vec
    perp_vec = point_vec .- proj
    return norm(perp_vec)
end

new_coord = [-118.4560 33.9637] #top right
dist_to_left_line = point_to_line_distance(corner_coords[1], corner_coords[2], new_coord)
dist_to_bottom_line = point_to_line_distance(corner_coords[2], corner_coords[3], new_coord)

pixel_x = round((dist_to_left_line / lon_per_pixel)/1.278) #wierd factor
pixel_y = round((dist_to_bottom_line / lat_per_pixel)/1.278) #wierd factor
println(String("Y: $(pixel_x)"))
println(String("X: $(pixel_y)"))

heatmap(normalized_band, c=:viridis, aspect_ratio=:equal)
scatter!([pixel_x], [pixel_y], c=:red, marker=:circle, markersize=5)
display(plot!)
