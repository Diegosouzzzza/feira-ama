# Geometry check script
conveyor_len = 700.0  # -350 to +350
conveyor_width = 150.0  # Z = -75 to +75
belt_width = 122.0  # Z = -61 to +61
drum_diam = 60.0  # R = 30
drum_centers_x = [-325.0, 325.0]  # distance 650 mm
drum_center_y = 80.0

top_belt_y = drum_center_y + 30.0 + 2.5 # 112.5 mm
bottom_belt_y = drum_center_y - 30.0 # 50.0 mm
bed_plate_y = 105.0 # bed plate supports belt from underneath
rail_top_y = 124.0 # 11.5 mm above belt surface (112.5)

print(f"Top belt surface Y: {top_belt_y} mm")
print(f"Bottom belt return Y: {bottom_belt_y} mm")
print(f"Guide rail top Y: {rail_top_y} mm (height above belt: {rail_top_y - top_belt_y} mm)")
print(f"Bed plate Y: {bed_plate_y} mm (clearance to belt top: {top_belt_y - bed_plate_y} mm)")
print(f"Conveyor span: {drum_centers_x[1] - drum_centers_x[0]} mm between drum axes")
