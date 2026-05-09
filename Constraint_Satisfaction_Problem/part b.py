import matplotlib.pyplot as plt
import networkx as nx

# 17 Sub-Counties of Nairobi
regions = [
    'Westlands', 'Dagoretti North', 'Dagoretti South', 'Langata', 'Kibra',
    'Roysambu', 'Kasarani', 'Ruaraka', 'Starehe', 'Mathare',
    'Kamukunji', 'Makadara', 'Embakasi West', 'Embakasi South',
    'Embakasi Central', 'Embakasi North', 'Embakasi East'
]

# Adjacency list based on geographic boundaries
neighbors = {
    'Westlands':        ['Dagoretti North', 'Roysambu', 'Starehe'],
    'Dagoretti North':  ['Westlands', 'Dagoretti South', 'Kibra', 'Starehe', 'Langata'],
    'Dagoretti South':  ['Dagoretti North', 'Kibra', 'Langata'],
    'Langata':          ['Dagoretti North', 'Dagoretti South', 'Kibra', 'Embakasi West'],
    'Kibra':            ['Dagoretti North', 'Dagoretti South', 'Langata', 'Starehe', 'Makadara'],
    'Roysambu':         ['Westlands', 'Kasarani', 'Ruaraka', 'Starehe'],
    'Kasarani':         ['Roysambu', 'Ruaraka', 'Embakasi North'],
    'Ruaraka':          ['Roysambu', 'Kasarani', 'Mathare', 'Starehe', 'Embakasi North'],
    'Starehe':          ['Westlands', 'Dagoretti North', 'Kibra', 'Roysambu', 'Ruaraka',
                         'Mathare', 'Kamukunji', 'Makadara'],
    'Mathare':          ['Ruaraka', 'Starehe', 'Kamukunji', 'Embakasi North'],
    'Kamukunji':        ['Starehe', 'Mathare', 'Makadara', 'Embakasi South'],
    'Makadara':         ['Kibra', 'Starehe', 'Kamukunji', 'Embakasi West',
                         'Embakasi South', 'Embakasi Central'],
    'Embakasi West':    ['Langata', 'Makadara', 'Embakasi South', 'Embakasi Central'],
    'Embakasi South':   ['Kamukunji', 'Makadara', 'Embakasi West',
                         'Embakasi Central', 'Embakasi East'],
    'Embakasi Central': ['Makadara', 'Embakasi West', 'Embakasi South',
                         'Embakasi North', 'Embakasi East'],
    'Embakasi North':   ['Kasarani', 'Ruaraka', 'Mathare',
                         'Embakasi Central', 'Embakasi East'],
    'Embakasi East':    ['Embakasi South', 'Embakasi Central', 'Embakasi North'],
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
def colour_map(index, colours):
    if index == len(regions):
        return True
    region = regions[index]
    for colour in colours:
        if is_valid(region, colour):
            solution[region] = colour
            if colour_map(index + 1, colours):
                return True
            del solution[region]
    return False

# Find minimum number of colours needed
colours_used = None
for n in range(2, 6):
    colour_options = ['Blue', 'Red', 'Green', 'Yellow', 'Purple'][:n]
    solution.clear()
    if colour_map(0, colour_options):
        colours_used = colour_options
        break

print("Solution:")
for region, colour in solution.items():
    print(f"  {region} = {colour}")
print(f"\nMinimum colours needed: {len(colours_used)}")

# Colour hex values
colour_hex = {
    'Blue':   '#2980b9',
    'Red':    '#e74c3c',
    'Green':  '#27ae60',
    'Yellow': '#f39c12',
    'Purple': '#8e44ad',
}

# Build graph
G = nx.Graph()
for region, adj in neighbors.items():
    for neighbor in adj:
        G.add_edge(region, neighbor)

# Geographic positions (approximate real-world layout)
pos = {
    'Westlands':        (1.5, 8.5),
    'Roysambu':         (4.0, 9.2),
    'Kasarani':         (6.5, 9.0),
    'Ruaraka':          (6.2, 7.5),
    'Dagoretti North':  (2.2, 7.0),
    'Starehe':          (4.2, 7.2),
    'Mathare':          (5.8, 6.8),
    'Dagoretti South':  (1.5, 5.5),
    'Kibra':            (3.0, 5.8),
    'Kamukunji':        (5.2, 5.5),
    'Embakasi North':   (7.5, 6.5),
    'Langata':          (1.8, 3.5),
    'Makadara':         (4.5, 4.5),
    'Embakasi West':    (3.2, 3.2),
    'Embakasi South':   (5.5, 3.2),
    'Embakasi Central': (6.8, 4.5),
    'Embakasi East':    (7.8, 3.2),
}

node_colors = [colour_hex[solution[n]] for n in G.nodes()]

fig, ax = plt.subplots(figsize=(14, 11))
fig.patch.set_facecolor('#1a1a2e')
ax.set_facecolor('#1a1a2e')

# Draw edges
nx.draw_networkx_edges(
    G, pos, ax=ax,
    edge_color='#aaaaaa',
    width=2.0,
    alpha=0.6
)

# Draw nodes
nx.draw_networkx_nodes(
    G, pos, ax=ax,
    node_color=node_colors,
    node_size=2800,
    alpha=0.95,
    linewidths=2,
    edgecolors='white'
)

# Draw labels — shorten long names
labels = {
    n: n.replace('Dagoretti ', 'Dag.\n')
        .replace('Embakasi ', 'Emb.\n')
    for n in G.nodes()
}
nx.draw_networkx_labels(
    G, pos, labels=labels, ax=ax,
    font_size=7.5,
    font_color='white',
    font_weight='bold'
)

ax.set_title(
    'Nairobi Sub-County Map Colouring', color='white', fontsize=18, fontweight='bold'
)
ax.axis('off')
plt.tight_layout()
plt.show()
print("Graph saved!")