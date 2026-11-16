from PIL import Image

# Let's crop screenshot_aba3_geral.png to see the symbols in full detail
im = Image.open(r"scratch\screenshot_aba3_geral.png")
w, h = im.size

# The SVG is drawn within the canvas
# Let's crop the right section: Motor, Diodes, LEDs, MOSFET, Q1, Buzzer
# In a 1920x1080 screen:
# Motor M13, E05, H05 are at the right side
crop_right = im.crop((int(w * 0.70), int(h * 0.40), int(w * 0.95), int(h * 0.90)))
crop_right.save(r"scratch\crop_right_symbols.png")
print("Saved crop_right_symbols.png")

# Center section: Relay K1, E09, Q2, E-STOP E12-B
crop_center = im.crop((int(w * 0.58), int(h * 0.42), int(w * 0.75), int(h * 0.78)))
crop_center.save(r"scratch\crop_center_symbols.png")
print("Saved crop_center_symbols.png")

# Left section: Fuses E16, Capacitor E06
crop_left = im.crop((int(w * 0.15), int(h * 0.42), int(w * 0.30), int(h * 0.85)))
crop_left.save(r"scratch\crop_left_symbols.png")
print("Saved crop_left_symbols.png")
