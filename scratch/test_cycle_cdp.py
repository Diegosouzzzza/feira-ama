import sys
sys.stdout.reconfigure(encoding='utf-8')
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

    print("--- Testing runFullCycle('rejected') ---")
    eval_js("runFullCycle('rejected')")
    sim_active = eval_js("simCycle.active")
    sim_mode = eval_js("simCycle.mode")
    belt_running = eval_js("isBeltRunning")
    status_text = eval_js("document.getElementById('actionStatus').textContent")
    print(f"simCycle.active={sim_active}, mode={sim_mode}, isBeltRunning={belt_running}")
    print(f"Status text: {status_text.encode('ascii', 'replace').decode('ascii')}")
    assert sim_active == True
    assert sim_mode == 'rejected'
    assert belt_running == True

    # Wait a bit for simulation progress
    time.sleep(1)
    stage = eval_js("simCycle.stage")
    fruit_x = eval_js("simCycle.fruitX")
    print(f"After 1s: stage={stage}, fruitX={fruit_x}")
    assert fruit_x > -340

    print("\n--- Testing runFullCycle('good') ---")
    eval_js("runFullCycle('good')")
    sim_mode_good = eval_js("simCycle.mode")
    print(f"simCycle.mode={sim_mode_good}")
    assert sim_mode_good == 'good'

    print("\nSimulation tests PASSED!")
finally:
    proc.terminate()
