import networkx as nx
import numpy as np
from PIL import Image

def image_to_graph(filepath, epsilon=0.01):
    pixels = np.array(Image.open(filepath).convert("L"), dtype=float) / 255.0
    rows, cols = pixels.shape
    G = nx.grid_2d_graph(rows, cols)
    for (r1, c1), (r2, c2) in G.edges():
        diff = abs(pixels[r1, c1] - pixels[r2, c2])
        G[r1, c1][r2, c2]["weight"] = 1.0 / (epsilon + diff)
    return G
 
if __name__ == "__main__":
    import os
    for filename in os.listdir("dat"):
        if filename.endswith(".png"):
            G = image_to_graph(f"dat\\{filename}")
            print(f"{filename:<20}:{len(G.nodes):>6} nodes, {len(G.edges):>6} edges")
