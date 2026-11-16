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
    "--remote-debugging-port=9222",
    "--window-size=1920,1080",
    "--allow-file-access-from-files",
    file_url
])

time.sleep(3)

try:
    resp = urllib.request.urlopen("http://127.0.0.1:9222/json")
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
    with open(r"scratch\screenshot_aba3_all_nobg.png", "wb") as f:
        f.write(base64.b64decode(res["result"]["data"]))
    print("Saved screenshot_aba3_all_nobg.png")

    ws.close()
finally:
    proc.terminate()

im = Image.open(r"scratch\screenshot_aba3_all_nobg.png")
w, h = im.size

# 1. Crop E15 (Disjuntor) and E01 (Fonte)
crop_e15_e01 = im.crop((int(w * 0.05), int(h * 0.40), int(w * 0.28), int(h * 0.65)))
crop_e15_e01.save(r"scratch\crop_e15_e01.png")
print("Saved crop_e15_e01.png")

# 2. Crop X1 and Bucks E02/E03
crop_x1_bucks = im.crop((int(w * 0.12), int(h * 0.55), int(w * 0.32), int(h * 0.90)))
crop_x1_bucks.save(r"scratch\crop_x1_bucks.png")
print("Saved crop_x1_bucks.png")

# 3. Crop Sensors S1/S2 and Terminal X2
crop_sensors_x2 = im.crop((int(w * 0.28), int(h * 0.40), int(w * 0.48), int(h * 0.78)))
crop_sensors_x2.save(r"scratch\crop_sensors_x2.png")
print("Saved crop_sensors_x2.png")
