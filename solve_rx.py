import math

# We want:
# y1*cos(rx) - z1*sin(rx) + py = Y_target
# y1*sin(rx) + z1*cos(rx) + pz = Z_target

# where z1 = -z (because ry = pi).
# For top: y1 = 120, z1 = -52.27 -> Target Y = 108, Z = 68
# For bot: y1 = 0, z1 = 52.27 -> Target Y = 56, Z = 168

# Difference:
# Delta Y = (120*cos(rx) + 52.27*sin(rx)) - (-52.27*sin(rx)) = 120*cos(rx) + 104.54*sin(rx) = 108 - 56 = 52
# Delta Z = (120*sin(rx) - 52.27*cos(rx)) - (52.27*cos(rx)) = 120*sin(rx) - 104.54*cos(rx) = 68 - 168 = -100

# Let's solve for rx:
for deg in range(-90, 90):
    rx = math.radians(deg)
    dY = 120 * math.cos(rx) + 104.54 * math.sin(rx)
    dZ = 120 * math.sin(rx) - 104.54 * math.cos(rx)
    err = (dY - 52)**2 + (dZ - (-100))**2
    if err < 500:
        print(f"deg={deg}: dY={dY:.1f}, dZ={dZ:.1f}, err={err:.1f}")
