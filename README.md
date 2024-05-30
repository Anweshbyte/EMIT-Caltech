# EMIT Data extraction using the CMR APIs

## Introduction
The Earth Surface Mineral Dust Source Investigation (EMIT) data can be accessed programmatically using NASA's Common Metadata Repository (CMR) API. The CMR is a metadata system that catalogs Earth Science data and associated metadata records. The CMR API allows users to search through its vast metadata holdings using various parameters and keywords. The following code builds the concept ID:

'''Julia
doi = "10.5067/EMIT/EMITL2ARFL.001"
cmrurl = "https://cmr.earthdata.nasa.gov/search/"
doisearch = cmrurl * "collections.json?doi=" * doi
response1 = HTTP.get(doisearch)
json_response = JSON.parse(String(response1.body))
concept_id = json_response["feed"]["entry"][1]["id"]

## Concept ID and DOI
To search for the EMIT dataset, you need NASA EarthData's unique Concept ID for the dataset. This Concept ID can be obtained using the Digital Object Identifier (DOI) for the dataset. DOIs can be found by clicking the `Citation` link on the [LP DAAC's EMIT Product Pages](https://lpdaac.usgs.gov/product_search/?query=emit&view=cards&sort=title).

### Concept ID for EMIT L2A Reflectance Dataset
The unique NASA-given Concept ID for the EMIT L2A Reflectance dataset is essential for retrieving relevant files (or granules).

## Handling Pagination
The CMR API has a limit of 2000 results per page and a maximum of 1 million granules matched. To handle pagination, use the `page_num` parameter to loop through the search result pages.

## Creating a DataFrame with the Resulting Links
A 'DataFrame` can be used to store the download URLs and geometries of each file. The EMIT L2A Reflectance and Uncertainty and Mask collection contains three assets per granule: reflectance, reflectance uncertainty, and masks. By printing the list, you can see the three assets corresponding to a single polygon.

### Exploding the DataFrame
To place each of these assets in a separate row, you can 'explode' the DataFrame. If you only want a subset of these assets, you can filter them out.

## Example Code
Below is an example of how to implement the above steps in Python.

```python
import requests
import pandas as pd

# Define the search endpoint and parameters
cmr_url = "https://cmr.earthdata.nasa.gov/search/granules"
concept_id = "YOUR_CONCEPT_ID"
params = {
    "concept_id": concept_id,
    "page_size": 2000,
    "page_num": 1,
    "bounding_box": "lon1,lat1,lon2,lat2",
    "temporal": "start_time,end_time"
}

# Function to query CMR and get results
def query_cmr(url, params):
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()

# Initialize an empty DataFrame
df = pd.DataFrame()

# Loop through the pages
while True:
    results = query_cmr(cmr_url, params)
    if not results['feed']['entry']:
        break
    df = df.append(pd.json_normalize(results['feed']['entry']))
    params['page_num'] += 1

# Explode the DataFrame to separate each asset
df_exploded = df.explode('links')

# Filter the DataFrame for the required assets
filtered_df = df_exploded[df_exploded['links.title'].str.contains("reflectance")]

# Display the DataFrame
print(filtered_df)
