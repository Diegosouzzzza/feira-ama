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

    # Switch to Aba 3 and toggle light theme
    send_cmd("Runtime.evaluate", {"expression": "switchTab('planta'); toggleTheme();"})
    time.sleep(1)

    # Screenshot general light
    res = send_cmd("Page.captureScreenshot", {"format": "png"})
    with open(r"scratch\screenshot_aba3_light.png", "wb") as f:
        f.write(base64.b64decode(res["result"]["data"]))
    print("Saved screenshot_aba3_light.png")

    ws.close()
finally:
    proc.terminate()

# Crop right section in light mode
im = Image.open(r"scratch\screenshot_aba3_light.png")
w, h = im.size
crop_right = im.crop((int(w * 0.70), int(h * 0.40), int(w * 0.95), int(h * 0.90)))
crop_right.save(r"scratch\crop_right_light.png")
print("Saved crop_right_light.png")
