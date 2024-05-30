# EMIT Data extraction using the CMR APIs

## Introduction
The Earth Surface Mineral Dust Source Investigation (EMIT) data can be accessed programmatically using NASA's Common Metadata Repository (CMR) API. The CMR is a metadata system that catalogs Earth Science data and associated metadata records. The CMR API allows users to search through its vast metadata holdings using various parameters and keywords. The following code builds the concept ID:

'''doi = "10.5067/EMIT/EMITL2ARFL.001"
cmrurl = "https://cmr.earthdata.nasa.gov/search/"
doisearch = cmrurl * "collections.json?doi=" * doi
response1 = HTTP.get(doisearch)
json_response = JSON.parse(String(response1.body))
concept_id = json_response["feed"]["entry"][1]["id"]'''

## Concept ID and DOI
To search for the EMIT dataset, you need NASA EarthData's unique Concept ID for the dataset. This Concept ID can be obtained using the Digital Object Identifier (DOI) for the dataset. DOIs can be found by clicking the `Citation` link on the [LP DAAC's EMIT Product Pages](https://lpdaac.usgs.gov/product_search/?query=emit&view=cards&sort=title).

### Concept ID for EMIT L2A Reflectance Dataset
The unique NASA-given Concept ID for the EMIT L2A Reflectance dataset is essential for retrieving relevant files (or granules).

## Handling Pagination
The CMR API has a limit of 2000 results per page and a maximum of 1 million granules matched. To handle pagination, use the `page_num` parameter to loop through the search result pages.

## Creating a DataFrame with the Resulting Links
A 'DataFrame` can be used to store the download URLs and geometries of each file. The EMIT L2A Reflectance and Uncertainty and Mask collection contains three assets per granule: reflectance, reflectance uncertainty, and masks. By printing the list, you can see the three assets corresponding to a single polygon.
