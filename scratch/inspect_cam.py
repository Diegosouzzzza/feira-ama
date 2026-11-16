import subprocess
import time
import json
import urllib.request
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

    info = eval_js("""
    (() => {
        return {
            camPos: [camera.position.x, camera.position.y, camera.position.z],
            target: [controls.target.x, controls.target.y, controls.target.z],
            zoom: camera.zoom,
            left: camera.left,
            right: camera.right,
            top: camera.top,
            bottom: camera.bottom,
            near: camera.near,
            far: camera.far
        };
    })()
    """)
    print("Camera info:", info)

finally:
    proc.terminate()
