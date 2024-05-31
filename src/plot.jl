using Pkg
# Pkg.add("Plotly")
# Pkg.add("NCDatasets")
using NCDatasets

nc_file_path = "/Users/arpitasen/Desktop/Sanghavi/Data/EMIT_L2A_RFL_001_20220903T163129_2224611_012.nc"
ncfile = NCDataset(nc_file_path, "r")
ref = ncfile["reflectance"]