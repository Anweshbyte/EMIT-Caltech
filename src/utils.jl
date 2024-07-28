using NCDatasets
using Statistics

function radiance_dep(file_path::AbstractString, pixel_x::Int, pixel_y::Int, start_band::Int, end_band::Int)
    ds = Dataset(file_path, "r")
    radiance = ds["radiance"][:]
    point_radiance = radiance[:, pixel_x, pixel_y]
    close(ds)
    
    num_bands = length(point_radiance)
    group_size = 5
    
    normalized_radiance = similar(point_radiance)
    
    for i in 1:num_bands
        group_start = max(1, i - div(group_size, 2))
        group_end = min(num_bands, i + div(group_size, 2))
        group_values = point_radiance[group_start:group_end]
        max_indices = sortperm(group_values, rev=true)[1:2]
        mean_max_values = mean(group_values[max_indices])
        normalized_radiance[i] = point_radiance[i] / mean_max_values
    end
    
    return normalized_radiance[start_band:end_band]
end