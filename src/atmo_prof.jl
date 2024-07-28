using NCDatasets
using YAML

function compute_atmos_profile_fields(T::AbstractArray{FT,1}, p_half::AbstractArray{FT,1}, q, vmr; g₀=9.807) where FT
    #@show "Atmos",  FT 
    # Floating type to use
    #FT = eltype(T)
    Nₐ = FT(6.02214179e+23)
    R  = FT(8.3144598)
    # Calculate full pressure levels
    p_full = (p_half[2:end] + p_half[1:end-1]) / 2

    # Dry and wet mass
    dry_mass = FT(28.9644e-3)    # in kg/molec, weighted average for N2 and O2
    wet_mass = FT(18.01534e-3)   # just H2O
    n_layers = length(T)

    # Also get a VMR vector of H2O (volumetric!)
    vmr_h2o = zeros(FT, n_layers, )
    vcd_dry = zeros(FT, n_layers, )
    vcd_h2o = zeros(FT, n_layers, )
    Δz      = zeros(FT, n_layers)
    # Now actually compute the layer VCDs
    for i = 1:n_layers 
        Δp = p_half[i + 1] - p_half[i]
        vmr_h2o[i] = dry_mass/(dry_mass-wet_mass*(1-1/q[i]))
        vmr_dry = 1 - vmr_h2o[i]
        M  = vmr_dry * dry_mass + vmr_h2o[i] * wet_mass
        vcd = Nₐ * Δp / (M  * g₀ * 100^2) * 100
        vcd_dry[i] = vmr_dry    * vcd   # includes m2->cm2
        vcd_h2o[i] = vmr_h2o[i] * vcd
        Δz[i] =  (log(p_half[i + 1]) - log(p_half[i])) / (g₀ * M  / (R * T[i]) )
        #@show Δz, T[i], M, Δp
    end

    # TODO: This is still a bit clumsy:
    new_vmr = Dict{String, Union{Real, Vector}}()

    for molec_i in keys(vmr)
        if vmr[molec_i] isa AbstractArray
            
            pressure_grid = collect(range(minimum(p_full), maximum(p_full), length=length(vmr[molec_i])))
            interp_linear = LinearInterpolation(pressure_grid, vmr[molec_i])
            new_vmr[molec_i] = [interp_linear(x) for x in p_full]
        else
            new_vmr[molec_i] = vmr[molec_i]
        end
    end

    return p_full, p_half, vmr_h2o, vcd_dry, vcd_h2o, new_vmr, Δz

end

"""
    struct GeosData
    A struct to hold the data read from netCDF files.

    Fields:
    - data::Dict{String, Any}: A dictionary where the keys are internal variable names and the values are their corresponding data.
"""
struct GeosData
    data::Dict{String, Any}
end
"""
    loadGeos(config_path::String) -> GeosData

Load data from netCDF files based on the configuration specified in a YAML file.

Arguments:
- `config_path::String`: Path to the YAML configuration file.

Returns:
- `GeosData`: A struct containing the loaded data.

The YAML configuration file should specify the file paths and the variables to read, along with their internal variable names. It also ensures that the filenames are identical apart from the second string when split using '.'.
"""
function loadGeos(config_path::String)
    config = YAML.load_file(config_path)
    all_data = Dict{String, Any}()
    file_paths = [file_info["path"]  for file_info in config["files"]]

    # Test if all filenames are identical apart from the second string if split using '.'
    base_names = [split(filepath, ".") for filepath in file_paths]
    for i in 1:length(base_names) - 1
        @assert length(base_names[i]) == length(base_names[i+1]) "Filenames have different lengths when split."
        for j in 1:length(base_names[i])
            if j != 2
                @assert base_names[i][j] == base_names[i+1][j] "Filenames differ at component $j: $(base_names[i][j]) vs $(base_names[i+1][j])"
            end
        end 
    end
    
    for file_info in config["files"]
        file_path = file_info["path"]
        variables = file_info["variables"]
        ds = NCDataset(file_path)
    
        for (file_var, internal_var) in variables
            all_data[internal_var] = ds[file_var][:]
        end
    
        if haskey(file_info, "groups")
            groups = file_info["groups"]
            for (file_grp, internal_grp) in groups
                for (grp_key, grp_val) in internal_grp
                    try
                        all_data[grp_val] = ds[file_grp][grp_key][:]
                    catch e
                        @warn "Group key $grp_key not found in file group $file_grp. Skipping..."
                    end
                end
            end
        end
    
        close(ds)
    end
    return GeosData(all_data)
end

"""
    getColumnAverage(gas, dp) -> Array{Float64, 2}

Calculate the column average of a gas species.

Arguments:
- `gas`: The gas concentration array with dimensions (latitude, longitude, levels, time).
- `dp`: The pressure difference array.

Returns:
- `Array{Float64, 2}`: The column average of the gas species with dimensions (latitude, longitude).
"""

function getColumnAverage(gas, dp)
    xgas = zeros(size(gas, 1), size(gas, 2))
    for i in 1:size(gas, 1)
        for j in 1:size(gas, 2)
            xgas[i, j] = gas[i, j, :, 1]' * dp
        end
    end
    return xgas
end


"""
    getTroposphericColumnAverage(gas, dp, tropoLev) -> Array{Float64, 2}

Calculate the tropospheric column average of a gas species up to the tropopause level, accounting for non-integer tropopause levels.

Arguments:
- `gas`: The gas concentration array with dimensions (latitude, longitude, levels, time).
- `dp`: The pressure difference array.
- `tropoLev`: The tropopause level array with dimensions (latitude, longitude, time).

Returns:
- `Array{Float64, 2}`: The tropospheric column average of the gas species with dimensions (latitude, longitude).

The function handles non-integer tropopause levels by including the last level, weighted according to the fractional part of the tropopause level index.
"""
function getTroposphericColumnAverage(gas, dp, tropoLev)
    xgas = zeros(size(gas, 1), size(gas, 2))
    for i in 1:size(gas, 1)
        for j in 1:size(gas, 2)
            tropo_level = tropoLev[i, j, 1]
            int_level = floor(Int, tropo_level)
            frac_level = tropo_level - int_level

            if int_level > 0
                # Include all levels up to the integer part of tropo_level
                xgas[i, j] = gas[i, j, 1:int_level, 1]' * dp[1:int_level]
                # Add the fractional part of the next level
                if int_level < size(gas, 3)
                    xgas[i, j] += gas[i, j, int_level + 1, 1] * dp[int_level + 1] * frac_level
                end
                # Normalize by the sum of the included dp values
                dp_sum = sum(dp[1:int_level]) + dp[int_level + 1] * frac_level
                xgas[i, j] /= dp_sum
            else
                # If the tropo_level is less than or equal to the first level, use only the fractional part
                xgas[i, j] = gas[i, j, 1, 1] * dp[1] * frac_level
                xgas[i, j] /= dp[1] * frac_level
            end
        end
    end
    return xgas
end

"""
    computeColumnAveragingOperator(geos) -> Array{Float64}

Compute the column averaging operator `dp` from the Geos files.

Arguments:
- `geos::GeosData`: All Geos Data.

Returns:
- `Array{Float64}`: The column averaging operator `dp`.

This function computes the following:
1. `levi = ai / 1000 + bi`
2. `dp = abs.(diff(levi))`
3. Normalize `dp` by dividing by the sum of its elements (note, we currently use the "wet" dp)
"""
function computeColumnAveragingOperator(geos::GeosData) 
    ai = geos.data["hyai"][:];
    bi = geos.data["hybi"][:];
    levi = ai / 1000 .+ bi
    dp = abs.(diff(levi))
    dp /= sum(dp)
    return dp
end

geos_data = loadGeos("/Users/arpitasen/Documents/GitHub/EMIT-Caltech/src/GeosChem.yaml")

temp = geos_data.data["tair"]
press = geos_data.data("Met_PMIDDRY")
hum = geos_data.data("Met_SPHU")

T = temp[1,1,:,1]
p_half = press[1,1,:,1]
q = hum[1,1,:,1]
