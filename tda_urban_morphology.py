import os
import numpy as np
import matplotlib.pyplot as plt
import osmnx as ox
from sklearn.metrics.pairwise import euclidean_distances
from sklearn.preprocessing import StandardScaler
from ripser import ripser
from persim import plot_diagrams, wasserstein

# Create the 'images' directory if it doesn't exist
os.makedirs('images', exist_ok=True)

# Specify the cities and download the street network data
cities = ["New York, USA", "London, UK", "Paris, France"]
city_graphs = []
city_coords = []

for city in cities:
    graph = ox.graph_from_place(city, network_type="drive")
    city_graphs.append(graph)
    
    gdf_nodes, _ = ox.graph_to_gdfs(graph)
    node_coords = np.array([(node["y"], node["x"]) for node in gdf_nodes.to_dict("records")])
    city_coords.append(node_coords)

# Perform topological data analysis for each city
city_diagrams = []

for coords in city_coords:
    scaler = StandardScaler()
    coords_scaled = scaler.fit_transform(coords)
    
    distance_matrix = euclidean_distances(coords_scaled)
    diagrams = ripser(distance_matrix, maxdim=1)['dgms']
    city_diagrams.append(diagrams)

# Plot the persistence diagrams for each city
fig, axes = plt.subplots(1, len(cities), figsize=(20, 5))

for i, (city, diagrams) in enumerate(zip(cities, city_diagrams)):
    plot_diagrams(diagrams, ax=axes[i], show=False)
    axes[i].set_title(f"Persistence Diagrams - {city}")
    axes[i].set_xlabel("Birth")
    axes[i].set_ylabel("Death")

plt.tight_layout()
plt.savefig("images/tda_urban_morphology_comparison.png", dpi=300, bbox_inches="tight")

# Compute Wasserstein distances between cities
wasserstein_matrix = np.zeros((len(cities), len(cities)))

for i in range(len(cities)):
    for j in range(len(cities)):
        wasserstein_matrix[i, j] = wasserstein(city_diagrams[i][1], city_diagrams[j][1])

print("Wasserstein Distance Matrix:")
print(wasserstein_matrix)

# Plot the street networks for each city
fig, axes = plt.subplots(1, len(cities), figsize=(20, 10))

for i, (city, graph) in enumerate(zip(cities, city_graphs)):
    ox.plot_graph(graph, ax=axes[i], node_size=0, edge_linewidth=0.5, edge_color='gray')
    axes[i].set_title(f"Street Network - {city}")
    axes[i].axis('off')

plt.tight_layout()
plt.savefig("images/tda_urban_morphology_networks.png", dpi=300, bbox_inches="tight")