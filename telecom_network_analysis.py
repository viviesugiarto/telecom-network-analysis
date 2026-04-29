import networkx as nx
import matplotlib.pyplot as plt
import random

# 1. GENERATE GENERIC TELECOM NETWORK
G = nx.erdos_renyi_graph(n=12, p=0.3, seed=42)

# Assign random distances (km) to edges
for (u, v) in G.edges():
    G[u][v]['weight'] = random.randint(100, 800)

# 2. GENERIC SIGNAL AMPLIFICATION MODEL
def estimate_amplification(distance, span=100):
    """
    Estimate number of amplification units required
    based on generic span constraint.
    """
    return max(0, int(distance / span))

# 3. ROUTING ANALYSIS
source, target = 0, 10

print(f"--- Routing Analysis (Node {source} → {target}) ---")

try:
    paths = list(nx.shortest_simple_paths(G, source, target, weight='weight'))
    
    for i, path in enumerate(paths[:3]):
        total_distance = 0
        total_amp = 0
        
        for j in range(len(path) - 1):
            u, v = path[j], path[j+1]
            d = G[u][v]['weight']
            total_distance += d
            total_amp += estimate_amplification(d)
        
        print(f"Path {i+1}: {path}")
        print(f"   Distance: {total_distance} km")
        print(f"   Amplification Units: {total_amp}\n")

except:
    print("No available path")

# 4. NETWORK ANALYSIS (IMPORTANT FOR PHD)
print("\n--- Network Analysis ---")

degree = nx.degree_centrality(G)
betweenness = nx.betweenness_centrality(G)

top_degree = sorted(degree.items(), key=lambda x: x[1], reverse=True)[:3]
top_between = sorted(betweenness.items(), key=lambda x: x[1], reverse=True)[:3]

print("Top Degree Centrality Nodes:")
for node, val in top_degree:
    print(f"Node {node}: {val:.3f}")

print("\nTop Betweenness Centrality Nodes:")
for node, val in top_between:
    print(f"Node {node}: {val:.3f}")

# 5. FAILURE SIMULATION
print("\n--- Failure Simulation ---")
G_fail = G.copy()

node_to_remove = random.choice(list(G.nodes()))
G_fail.remove_node(node_to_remove)

print(f"Removed node: {node_to_remove}")

try:
    new_path = nx.shortest_path(G_fail, source, target, weight='weight')
    print(f"New path after failure: {new_path}")
except:
    print("Network disconnected after failure")

# 6. VISUALIZATION
plt.figure(figsize=(10, 7))
pos = nx.spring_layout(G)

nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=800)
labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

plt.title("Generic Telecom Network Graph (Synthetic)")
plt.show()