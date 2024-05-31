using NCDatasets

jan = Dataset("/Users/arpitasen/Desktop/Sanghavi/Data/EMIT_L1B_RAD_001_20231026T175210_2329912_009.nc")

# Print available variables
println(keys(jan))

# Extract radiance variable
reflectance = jan["radiance"]

# Define band range
start_band = 50 # Oxy - A Band
end_band = 50 # Oxy - A Band

# Select data for specified band range
reflectance_selected_bands = reflectance[start_band:end_band,:,:]
println("Shape of reflectance data for bands $start_band to $(end_band - 1): ", size(reflectance_selected_bands))
println(reflectance_selected_bands)