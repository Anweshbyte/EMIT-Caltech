using Pkg
# Pkg.add("Plotly")
# Pkg.add("NCDatasets")
using NCDatasets
nc_file_path = "/Users/arpitasen/Desktop/Sanghavi/Data/EMIT_L2A_RFL_001_20220903T163129_2224611_012.nc"
ncfile = NCDataset(nc_file_path, "r")
wv = ncfile["lon"]
# # println("Variables:")
# # for var in names(ncfile)
# #     println("  $var")
# # end
# # println("\nGroups:")
# # for grp in groupnames(ncfile)
# #     println("  $grp")
# # end
# # close(ncfile)
# ds = NCDataset(nc_file_path, "r")
# println(ds)
# ncvar_cf = ds["wavelengths"]
# data = Array(ncvar_cf)
# println(data)
# using Pkg
# Pkg.add("NetCDF")
# using NetCDF

# # Path to your NetCDF file
# file_path = "/Users/arpitasen/Desktop/Sanghavi/Data/EMIT_L2A_RFL_001_20220903T163129_2224611_012.nc"

# # Open the NetCDF file
# ncfile = NetCDF.open(file_path)
# print(ncfile)

# Access the 'wavelengths' variable
# wavelengths = ncfile["sensor_band_parameters"]["wavelengths"][:]

# # Close the NetCDF file
# NetCDF.close(ncfile)

# # Print the first few elements of the 'wavelengths' array
# println(wavelengths[1:5])


