using NCDatasets
using Plots

ds = Dataset("/Users/arpitasen/Desktop/Sanghavi/Data/EMIT_L1B_RAD_001_20231026T175210_2329912_009.nc", "r")
radiance = ds["radiance"][:]
point_radiance = radiance[:, 500, 500]
close(ds)
bands = 1:length(point_radiance)
plot(bands, point_radiance, xlabel="Bands", ylabel="Radiance", title="Radiance for point (500, 500) across all bands")
