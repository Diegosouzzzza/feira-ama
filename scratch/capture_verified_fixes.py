import subprocess
import time
import json
import urllib.request
import base64
import websocket
from PIL import Image

edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
file_url = r"file:///C:/Users/ponto/OneDrive/Desktop/FEIRA%20-%20AMA/desenho-eletrico/esp32.html"

proc = subprocess.Popen([
    edge_path,
    "--headless=new",
    "--remote-debugging-port=9224",
    "--window-size=1920,1080",
    "--allow-file-access-from-files",
    file_url
])

time.sleep(3)

try:
    resp = urllib.request.urlopen("http://127.0.0.1:9224/json")
    targets = json.loads(resp.read().decode())
    target = next(t for t in targets if t.get("type") == "page")
    ws_url = target["webSocketDebuggerUrl"]

    ws = websocket.create_connection(ws_url)

    def send_cmd(method, params=None):
        cmd = {"id": int(time.time()*1000) % 100000, "method": method, "params": params or {}}
        ws.send(json.dumps(cmd))
        while True:
            r = json.loads(ws.recv())
            if r.get("id") == cmd["id"]:
                return r

    # Switch to Aba 3
    send_cmd("Runtime.evaluate", {"expression": "switchTab('planta');"})
    time.sleep(1)

    # Screenshot general
    res = send_cmd("Page.captureScreenshot", {"format": "png"})
    with open(r"scratch\screenshot_verified_fixes.png", "wb") as f:
        f.write(base64.b64decode(res["result"]["data"]))
    print("Saved screenshot_verified_fixes.png")

    ws.close()
finally:
    proc.terminate()

im = Image.open(r"scratch\screenshot_verified_fixes.png")
w, h = im.size

# 1. Crop E15 and E01
crop1 = im.crop((int(w * 0.05), int(h * 0.40), int(w * 0.22), int(h * 0.60)))
crop1.save(r"scratch\verified_e15.png")

# 2. Crop S3 and K1
crop2 = im.crop((int(w * 0.60), int(h * 0.40), int(w * 0.75), int(h * 0.62)))
crop2.save(r"scratch\verified_s3_k1.png")

# 3. Crop ESP32 left pins GPIO26/27
crop3 = im.crop((int(w * 0.42), int(h * 0.48), int(w * 0.58), int(h * 0.70)))
crop3.save(r"scratch\verified_gpio26_27.png")

# 4. Crop W048/W050 area
crop4 = im.crop((int(w * 0.73), int(h * 0.45), int(w * 0.86), int(h * 0.75)))
crop4.save(r"scratch\verified_w048_w050.png")

print("All crops saved successfully!")
