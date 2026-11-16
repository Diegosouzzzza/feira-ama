import math

def transform_pt(x, y, z, rot_x, rot_y, rot_z, px, py, pz):
    cy, sy = math.cos(rot_y), math.sin(rot_y)
    x1 = x * cy + z * sy
    y1 = y
    z1 = -x * sy + z * cy
    cx, sx = math.cos(rot_x), math.sin(rot_x)
    x2 = x1
    y2 = y1 * cx - z1 * sx
    z2 = y1 * sx + z1 * cx
    return (x2 + px, y2 + py, z2 + pz)

top_raw = (0, 120, 52.27)
bot_raw = (0, 0, -52.27)

top_t = transform_pt(*top_raw, -0.46, math.pi, 0, 170, 7, 108)
bot_t = transform_pt(*bot_raw, -0.46, math.pi, 0, 170, 7, 108)

print("Transformed top:", top_t)
print("Transformed bot:", bot_t)
