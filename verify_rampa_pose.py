import math

def transform_pt(x, y, z, rx, ry, rz, px, py, pz):
    cy, sy = math.cos(ry), math.sin(ry)
    x1 = x * cy + z * sy
    y1 = y
    z1 = -x * sy + z * cy
    cx, sx = math.cos(rx), math.sin(rx)
    x2 = x1
    y2 = y1 * cx - z1 * sx
    z2 = y1 * sx + z1 * cx
    return (x2 + px, y2 + py, z2 + pz)

top_raw = (0, 120, 52.27)
bot_raw = (0, 0, -52.27)

rx = math.radians(-25)
ry = math.pi
pz = 138.0
py = 28.0
px = 170.0

top_t = transform_pt(*top_raw, rx, ry, 0, px, py, pz)
bot_t = transform_pt(*bot_raw, rx, ry, 0, px, py, pz)

print("Top point:", top_t)
print("Bottom point:", bot_t)
