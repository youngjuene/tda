import numpy as np
import matplotlib.pyplot as plt
import osmnx as ox
from sklearn.metrics.pairwise import euclidean_distances
from sklearn.preprocessing import StandardScaler
from ripser import ripser
from persim import plot_diagrams

# Specify the city and download the street network data
city = "New York, USA"
graph = ox.graph_from_place(city, network_type="drive")

# Convert the graph to a GeoDataFrame
gdf_nodes, gdf_edges = ox.graph_to_gdfs(graph)

# Extract the node coordinates
node_coords = np.array([(node["x"], node["y"]) for node in gdf_nodes.to_dict("records")])

# Standardize the node coordinates
scaler = StandardScaler()
node_coords_scaled = scaler.fit_transform(node_coords)

# Compute the distance matrix
distance_matrix = euclidean_distances(node_coords_scaled)

# Perform topological data analysis using Ripser
diagrams = ripser(distance_matrix, maxdim=1)['dgms']

# Plot the persistence diagrams
plt.figure(figsize=(8, 4))
plot_diagrams(diagrams, show=False)
plt.title("Persistence Diagrams - Urban Street Network")
plt.tight_layout()
plt.show()