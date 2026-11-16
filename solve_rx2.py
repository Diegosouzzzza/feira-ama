import math

for deg in range(-90, 90, 10):
    rx = math.radians(deg)
    dY = 120 * math.cos(rx) + 104.54 * math.sin(rx)
    dZ = 120 * math.sin(rx) - 104.54 * math.cos(rx)
    print(f"deg={deg:3d}: dY={dY:6.1f}, dZ={dZ:6.1f}")
