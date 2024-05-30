using Pkg
using CSV
using DataFrames
using Dates
using HTTP
using JSON
using Base.Iterators
using IterTools
using GeometryBasics
using Shapefile
using GeoJSON
using GeoInterface
using DataFrames
using SplitApplyCombine

doi = "10.5067/EMIT/EMITL2ARFL.001"
cmrurl = "https://cmr.earthdata.nasa.gov/search/"
doisearch = cmrurl * "collections.json?doi=" * doi
response1 = HTTP.get(doisearch)
json_response = JSON.parse(String(response1.body))
concept_id = json_response["feed"]["entry"][1]["id"]

start_date = DateTime(2022, 9, 3)
end_date = DateTime(2022, 9, 3, 23, 23, 59)
dt_format = dateformat"yyyy-mm-ddTHH:MM:SSZ"
start_str = Dates.format(start_date, dt_format)
end_str = Dates.format(end_date, dt_format)
temporal_str = start_str * "," * end_str

lon = -62.1123
lat = -39.89402
point_str = string(lon) * "," * string(lat)

page_num = 0
page_size = 2000 # CMR page size limit
granule_arr = []
output = DataFrame(Asset = String[], URL = [], CC = String[], Poly = [])
while true
    global page_num += 1
    cmr_param = Dict(
        "collection_concept_id" => concept_id,
        "page_size" => string(page_size),
        "page_num" => string(page_num),
        "temporal" => temporal_str,
        "point" => point_str
    )
    granulesearch = cmrurl * "granules.json"
    response = HTTP.post(granulesearch, [], HTTP.Form(cmr_param))
    granules = JSON.parse(String(response.body))["feed"]["entry"]
    if isempty(granules)  # Exit loop if no granules are returned
        break
    end
    for g in granules
        granule_urls = []
        global cloud_cover = get(g, "cloud_cover", "")
        if haskey(g, "polygons")
            polygons = get(g, "polygons", "")
            for poly in polygons
                terms = split(poly[1])
                ltln = []
                for i in 1:2:length(terms)-1
                    push!(ltln, terms[i] * " " * terms[i+1])
                end
                global granule_poly = [join(reverse(split(s, ' ')), ' ') for s in ltln]
            end
        end
        global granule_urls = [x["href"] for x in g["links"] if occursin("https", x["href"]) && occursin(".nc", x["href"]) && !occursin(".dmrpp", x["href"])]
    end
    df = DataFrame(URL = [granule_urls], CC = cloud_cover, Poly = [granule_poly])
    df = DataFrame(
    URL = vcat(df[!, "URL"]...),
    CC = repeat(df[!, "CC"], inner=length(df[!, "URL"][1])),
    Poly = repeat(df[!, "Poly"], inner=length(df[!, "URL"][1]))
    )
    df[!,"Asset"] = last.(split.(df[:, "URL"], '/'))

    # Reorder the columns if necessary
    df = df[:, ["Asset", setdiff(names(df), ["Asset"])...]]
    append!(output, df)
end

CSV.write("EMIT_extract.csv", output)