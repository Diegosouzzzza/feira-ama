# Verification of all 5 CAD parts positions and world bounding boxes
import math, json

with open('cad_data_preserved.json', 'r', encoding='utf-8') as f:
    cad_obj = json.load(f)

def get_world_bounds(verts, scale=(1,1,1), rot=(0,0,0), pos=(0,0,0)):
    sx, sy, sz = scale
    rx, ry, rz = rot
    px, py, pz = pos
    min_x, max_x = float('inf'), float('-inf')
    min_y, max_y = float('inf'), float('-inf')
    min_z, max_z = float('inf'), float('-inf')
    
    cx, sx_ = math.cos(rx), math.sin(rx)
    cy, sy_ = math.cos(ry), math.sin(ry)
    cz, sz_ = math.cos(rz), math.sin(rz)

    for i in range(0, len(verts), 3):
        x, y, z = verts[i]*sx, verts[i+1]*sy, verts[i+2]*sz
        # Rot Y
        x1 = x * cy + z * sy_
        y1 = y
        z1 = -x * sy_ + z * cy
        # Rot X
        x2 = x1
        y2 = y1 * cx - z1 * sx_
        z2 = y1 * sx_ + z1 * cx
        # Trans
        wx = x2 + px
        wy = y2 + py
        wz = z2 + pz
        min_x, max_x = min(min_x, wx), max(max_x, wx)
        min_y, max_y = min(min_y, wy), max(max_y, wy)
        min_z, max_z = min(min_z, wz), max(max_z, wz)
    return (min_x, max_x), (min_y, max_y), (min_z, max_z)

# 1. caixaApp
app_b = get_world_bounds(cad_obj['caixa']['verts'], pos=(435, 0, 0))
print("caixaApp bounds:", app_b)
# 2. caixaRej
rej_b = get_world_bounds(cad_obj['caixa']['verts'], pos=(170, 0, 195))
print("caixaRej bounds:", rej_b)
# 3. pa (rest)
pa_b = get_world_bounds(cad_obj['pa']['verts'], scale=(1, 0.55, 1), pos=(160, 113.5, -61))
print("pa bounds (rest):", pa_b)
# 4. suporte_servo
ss_b = get_world_bounds(cad_obj['suporte_servo']['verts'], rot=(0, math.pi/2, 0), pos=(160, 89, 0))
print("suporte_servo bounds:", ss_b)
# 5. rampa
rampa_b = get_world_bounds(cad_obj['rampa']['verts'], rot=(math.radians(-25), math.pi, 0), pos=(170, 22, 162))
print("rampa bounds:", rampa_b)
# 6. suporte_sensor S1
s1_b = get_world_bounds(cad_obj['suporte_sensor']['verts'], pos=(-150, 30, -76))
print("suporte_sensor S1 bounds:", s1_b)
