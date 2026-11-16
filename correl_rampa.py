import json

with open('cad_data_preserved.json', 'r', encoding='utf-8') as f:
    cad_obj = json.load(f)

v = cad_obj['rampa']['verts']
pts = [(v[i], v[i+1], v[i+2]) for i in range(0, len(v), 3)]

# Correlation between Y and Z
sum_y = sum(p[1] for p in pts)
sum_z = sum(p[2] for p in pts)
n = len(pts)
mean_y = sum_y / n
mean_z = sum_z / n

cov = sum((p[1] - mean_y) * (p[2] - mean_z) for p in pts)
var_y = sum((p[1] - mean_y)**2 for p in pts)
var_z = sum((p[2] - mean_z)**2 for p in pts)
corr = cov / ((var_y * var_z)**0.5)

print(f"Mean Y: {mean_y:.1f}, Mean Z: {mean_z:.1f}")
print(f"Correlation between Y and Z: {corr:.3f}")

# Let's find vertices with highest Y and lowest Y
sorted_by_y = sorted(pts, key=lambda p: p[1])
print("Lowest Y:", sorted_by_y[0], sorted_by_y[1])
print("Highest Y:", sorted_by_y[-1], sorted_by_y[-2])
