from PIL import Image

im = Image.open(r"scratch\screenshot_aba3_all_nobg.png")
w, h = im.size

# Crop Right side: Relay, Servo, MOSFET, Motor, LEDs
crop_right = im.crop((int(w * 0.55), int(h * 0.35), int(w * 0.98), int(h * 0.85)))
crop_right.save(r"scratch\crop_right_unboxed.png")
print("Saved crop_right_unboxed.png")
