using NCDatasets
using Plots

dataset = Dataset("/home/cfranken/data/GeosChem/Benchmark/GEOSChem.StateMet.20190101_0000z.nc4")
println(dataset)
# println("Variables in the NetCDF file:")
# for name in keys(dataset)
#     println(name)
# end

# var_name = "AerNumDensityStratParticulate"
# nc_var = dataset[var_name]
# data = nc_var[:]
# close(dataset)

# println(size(data))

# prof = data[1,1,:,1]
# plot(prof)
