import csv
import os
import requests
from netCDF4 import Dataset
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import matplotlib.path as mpath

# Step 1: Read the CSV file
def read_csv(file_path):
    links_and_coords = []
    with open(file_path, mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            link = row['URL']
            coordinates = eval(row['Poly'])
            links_and_coords.append((link, coordinates))
    return links_and_coords

# Step 2: Download NetCDF file
def download_file(url, dest_folder):
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)
    file_name = os.path.join(dest_folder, url.split('/')[-1])
    response = requests.get(url)
    with open(file_name, 'wb') as file:
        file.write(response.content)
    return file_name

# Step 3: Extract radiance values
def extract_radiance(file_path):
    nc = Dataset(file_path, mode='r')
    radiance = nc.variables['radiance'][:]
    nc.close()
    return radiance

# Step 4: Normalize the selected band and create heatmap
def plot_heatmap_with_polygon(radiance_band, coordinates):
    # Normalize the radiance band
    radiance_normalized = radiance_band / np.max(radiance_band)
    
    # Plot heatmap
    plt.imshow(radiance_normalized, cmap='hot', interpolation='nearest')
    plt.colorbar(label='Normalized Radiance')

    # Convert coordinates to pixel space (for simplicity, assuming the coordinates can be mapped linearly)
    # This part should be adjusted based on actual mapping of coordinates to pixel space
    x_coords = [coord.split()[0] for coord in coordinates[:-1]]
    y_coords = [coord.split()[1] for coord in coordinates[:-1]]

    x_coords = np.array(x_coords, dtype=float)
    y_coords = np.array(y_coords, dtype=float)

    # Create polygon
    polygon_points = np.array([x_coords, y_coords]).T
    polygon = Polygon(polygon_points, closed=True, edgecolor='blue', fill=False, linewidth=2)

    # Add polygon to the plot
    plt.gca().add_patch(polygon)
    plt.title('Heatmap with Region Marked')
    plt.xlabel('Pixel X')
    plt.ylabel('Pixel Y')
    plt.show()

# Main function to run all steps
def main(csv_file, band_number, dest_folder='./netcdf_files'):
    links_and_coords = read_csv(csv_file)

    for link, coordinates in links_and_coords:
        file_path = download_file(link, dest_folder)
        radiance = extract_radiance(file_path)
        radiance_band = radiance[:, :, band_number]
        plot_heatmap_with_polygon(radiance_band, coordinates)

csv_file = 'EMIT_extract.csv'  # Path to your CSV file
band_number = 52  # Change this to select the band number
main(csv_file, band_number)
