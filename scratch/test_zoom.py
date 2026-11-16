import subprocess
import time
import json
import urllib.request
import base64
import websocket

edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
file_url = r"file:///C:/Users/ponto/OneDrive/Desktop/FEIRA%20-%20AMA/Manual_Montagem_Esteira_70cm.html"

proc = subprocess.Popen([
    edge_path,
    "--headless=new",
    "--remote-debugging-port=9222",
    "--window-size=1600,1000",
    "--allow-file-access-from-files",
    file_url
])

time.sleep(3)

try:
    resp = urllib.request.urlopen("http://127.0.0.1:9222/json")
    targets = json.loads(resp.read().decode())
    target = [t for t in targets if "Manual_Montagem_Esteira_70cm.html" in t.get("url", "")][0]
    ws = websocket.create_connection(target["webSocketDebuggerUrl"])

    req_id = 1
    def send_cmd(method, params=None):
        global req_id
        msg = {"id": req_id, "method": method}
        if params: msg["params"] = params
        req_id += 1
        ws.send(json.dumps(msg))
        while True:
            res = json.loads(ws.recv())
            if res.get("id") == msg["id"]:
                return res

    send_cmd("Runtime.enable")
    def eval_js(expr):
        res = send_cmd("Runtime.evaluate", {"expression": expr, "returnByValue": True})
        return res.get("result", {}).get("result", {}).get("value")

    eval_js("setViewMode('fair')")
    time.sleep(0.5)

    # Check bounds of bancaFeiraGroup
    banca_box = eval_js("""
    (() => {
        const box = new THREE.Box3().setFromObject(bancaFeiraGroup);
        return {
            min: [box.min.x, box.min.y, box.min.z],
            max: [box.max.x, box.max.y, box.max.z]
        };
    })()
    """)
    print("bancaFeiraGroup bounding box:", banca_box)

    # Let's see what camera is
    cam_type = eval_js("camera.constructor.name")
    cam_zoom = eval_js("camera.zoom")
    print(f"Camera type: {cam_type}, zoom: {cam_zoom}")

    # Test with zoom = 0.48 to fit whole fair booth
    eval_js("camera.zoom = 0.48; camera.updateProjectionMatrix();")
    time.sleep(0.5)

    shot = send_cmd("Page.captureScreenshot", {"format": "png"})
    if "result" in shot and "data" in shot["result"]:
        img_data = base64.b64decode(shot["result"]["data"])
        with open("scratch/fair_screenshot_zoom_048.png", "wb") as sf:
            sf.write(img_data)
        with open(r"C:\Users\ponto\.gemini\antigravity\brain\9be8ac6e-57f1-4fbe-ac21-2749d1c9f4a3\fair_screenshot.png", "wb") as sf:
            sf.write(img_data)
        print("Zoom 0.48 screenshot saved!")

finally:
    proc.terminate()
