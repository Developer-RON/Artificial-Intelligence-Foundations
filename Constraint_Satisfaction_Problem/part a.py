import matplotlib.pyplot as plt
import networkx as nx

# Regions of Australia
regions = ['WA', 'NT', 'SA', 'Q', 'NSW']

# Available colours
colours = ['Blue', 'Red', 'Green']

# Adjacency list
neighbors = {
    'WA':  ['NT', 'SA'],
    'NT':  ['WA', 'SA', 'Q'],
    'SA':  ['WA', 'NT', 'Q', 'NSW'],
    'Q':   ['NT', 'SA', 'NSW'],
    'NSW': ['SA', 'Q'],
}

# Store colouring solution
solution = {}

# Check if colour assignment is valid
def is_valid(region, colour):
    for neighbor in neighbors.get(region, []):
        if neighbor in solution and solution[neighbor] == colour:
            return False
    return True

# Recursive backtracking function
def colour_map(index):
    if index == len(regions):
        return True
    region = regions[index]
    for colour in colours:
        if is_valid(region, colour):
            solution[region] = colour
            if colour_map(index + 1):
                return True
            del solution[region]
    return False

# Run colouring
colour_map(0)

print("Solution:")
for region, colour in solution.items():
    print(f"  {region} = {colour}")

# Colour hex values
colour_hex = {
    'Blue':  '#2980b9',
    'Red':   '#e74c3c',
    'Green': '#27ae60',
}

# Build graph
G = nx.Graph()
for region, adj in neighbors.items():
    for neighbor in adj:
        G.add_edge(region, neighbor)

# Geographic positions (approximate real-world layout of Australia)
pos = {
    'WA':  (1.5, 5.0),
    'NT':  (4.0, 7.0),
    'SA':  (4.5, 4.5),
    'Q':   (6.5, 6.5),
    'NSW': (6.5, 3.5),
}

node_colors = [colour_hex[solution[n]] for n in G.nodes()]

fig, ax = plt.subplots(figsize=(10, 7))
fig.patch.set_facecolor('#1a1a2e')
ax.set_facecolor('#1a1a2e')

# Draw edges
nx.draw_networkx_edges(
    G, pos, ax=ax,
    edge_color='#aaaaaa',
    width=2.5,
    alpha=0.6
)

# Draw nodes
nx.draw_networkx_nodes(
    G, pos, ax=ax,
    node_color=node_colors,
    node_size=3500,
    alpha=0.95,
    linewidths=2,
    edgecolors='white'
)

# Draw labels
nx.draw_networkx_labels(
    G, pos, ax=ax,
    font_size=13,
    font_color='white',
    font_weight='bold'
)

ax.set_title(
    'Australia Map Colouring', color='white', fontsize=18, fontweight='bold',  
)
ax.axis('off')
plt.tight_layout()
plt.show()
print("Graph saved!")