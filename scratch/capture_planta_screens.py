import subprocess
import time
import json
import urllib.request
import base64
import websocket

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

    # Screenshot 1: General view
    res = send_cmd("Page.captureScreenshot", {"format": "png"})
    with open(r"scratch\screenshot_aba3_geral.png", "wb") as f:
        f.write(base64.b64decode(res["result"]["data"]))
    print("Saved screenshot_aba3_geral.png")

    # Zoom into Right side: M13, E05, H05, E25, Q1
    send_cmd("Runtime.evaluate", {
        "expression": """
        const svg = document.getElementById('planta-geral');
        if (svg) {
            svg.setAttribute('viewBox', '1700 220 620 500');
        }
        """
    })
    time.sleep(1)
    res = send_cmd("Page.captureScreenshot", {"format": "png"})
    with open(r"scratch\screenshot_aba3_motor_diodes_leds.png", "wb") as f:
        f.write(base64.b64decode(res["result"]["data"]))
    print("Saved screenshot_aba3_motor_diodes_leds.png")

    # Zoom into Center-Left side: Relay E08, Diode E09, Q2, E12-B, E12-A, Clamps, Fuses E16
    send_cmd("Runtime.evaluate", {
        "expression": """
        const svg = document.getElementById('planta-geral');
        if (svg) {
            svg.setAttribute('viewBox', '1400 240 380 320');
        }
        """
    })
    time.sleep(1)
    res = send_cmd("Page.captureScreenshot", {"format": "png"})
    with open(r"scratch\screenshot_aba3_relay_q2_e09.png", "wb") as f:
        f.write(base64.b64decode(res["result"]["data"]))
    print("Saved screenshot_aba3_relay_q2_e09.png")

    # Zoom into Fuses E16 & Capacitor E06
    send_cmd("Runtime.evaluate", {
        "expression": """
        const svg = document.getElementById('planta-geral');
        if (svg) {
            svg.setAttribute('viewBox', '420 240 220 540');
        }
        """
    })
    time.sleep(1)
    res = send_cmd("Page.captureScreenshot", {"format": "png"})
    with open(r"scratch\screenshot_aba3_fuses_cap.png", "wb") as f:
        f.write(base64.b64decode(res["result"]["data"]))
    print("Saved screenshot_aba3_fuses_cap.png")

    ws.close()
finally:
    proc.terminate()
