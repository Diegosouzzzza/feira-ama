import math

# Test rampa transform
# Target: top lip at Y ~ 108, Z ~ 68. Bottom lip at Y ~ 57, Z ~ 165.
# Raw: Top has (x, 120, 52.27), Bottom has (x, 0, -52.27).

# Let's see: if we tilt or rotate:
# In Three.js:
# Suppose rampaGroup is placed at (posX, posY, posZ) with rotation:
# If rotated around Y by 180 deg:
# new_y = y, new_z = -z
# For top: raw y=120, z=52.27 -> new_y = 120, new_z = -52.27
# For bottom: raw y=0, z=-52.27 -> new_y = 0, new_z = 52.27
# Difference in Y: 120 mm. Difference in Z: 104.54 mm.
# Delta Y is 120, which is steep (from 108 down to -12).
# If we tilt rampa by -25 degrees around X:
# Let's test the matrix transform!

def transform_pt(x, y, z, rot_x, rot_y, rot_z, px, py, pz):
    # Apply rot_y
    cy, sy = math.cos(rot_y), math.sin(rot_y)
    x1 = x * cy + z * sy
    y1 = y
    z1 = -x * sy + z * cy
    # Apply rot_x
    cx, sx = math.cos(rot_x), math.sin(rot_x)
    x2 = x1
    y2 = y1 * cx - z1 * sx
    z2 = y1 * sx + z1 * cx
    return (x2 + px, y2 + py, z2 + pz)

# Test rot_y = PI, rot_x = -0.35 rad (~-20 deg), px = 170, py = 35, pz = 115
top_raw = (0, 120, 52.27)
bot_raw = (0, 0, -52.27)

top_t = transform_pt(*top_raw, -0.32, math.pi, 0, 170, 25, 115)
bot_t = transform_pt(*bot_raw, -0.32, math.pi, 0, 170, 25, 115)

print("Transformed top:", top_t)
print("Transformed bot:", bot_t)
