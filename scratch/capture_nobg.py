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
    with open(r"scratch\screenshot_aba3_nobg_geral.png", "wb") as f:
        f.write(base64.b64decode(res["result"]["data"]))
    print("Saved screenshot_aba3_nobg_geral.png")

    ws.close()
finally:
    proc.terminate()

im = Image.open(r"scratch\screenshot_aba3_nobg_geral.png")
w, h = im.size

# Crop H05 specifically (the part user asked about)
crop_h05 = im.crop((int(w * 0.77), int(h * 0.40), int(w * 0.96), int(h * 0.65)))
crop_h05.save(r"scratch\crop_h05_nobg.png")
print("Saved crop_h05_nobg.png")

# Crop Buzzer & Q1
crop_buzzer_q1 = im.crop((int(w * 0.77), int(h * 0.62), int(w * 0.96), int(h * 0.90)))
crop_buzzer_q1.save(r"scratch\crop_buzzer_q1_nobg.png")
print("Saved crop_buzzer_q1_nobg.png")

# Crop Center: Relay K1, Q2, E-STOP
crop_center = im.crop((int(w * 0.58), int(h * 0.42), int(w * 0.75), int(h * 0.78)))
crop_center.save(r"scratch\crop_center_nobg.png")
print("Saved crop_center_nobg.png")
