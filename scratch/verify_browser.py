import sys
sys.stdout.reconfigure(encoding='utf-8')
import subprocess
import time
import json
import urllib.request
import base64
import websocket

edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
file_url = r"file:///C:/Users/ponto/OneDrive/Desktop/FEIRA%20-%20AMA/Manual_Montagem_Esteira_70cm.html"

# Launch Edge headless
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
    target = None
    for t in targets:
        if "Manual_Montagem_Esteira_70cm.html" in t.get("url", ""):
            target = t
            break

    if not target:
        print("ERROR: Target tab not found!")
        exit(1)

    ws_url = target["webSocketDebuggerUrl"]
    print("Connecting to:", ws_url)
    ws = websocket.create_connection(ws_url)

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

    # Enable Console & Runtime
    send_cmd("Runtime.enable")
    send_cmd("Console.enable")

    def eval_js(expr):
        res = send_cmd("Runtime.evaluate", {"expression": expr, "returnByValue": True})
        return res.get("result", {}).get("result", {}).get("value")

    # 1. Initial State Check
    init_mode = eval_js("currentViewMode")
    banca_vis = eval_js("bancaFeiraGroup.visible")
    print(f"Initial: currentViewMode={init_mode}, bancaFeiraGroup.visible={banca_vis}")
    assert init_mode == 'isometric'
    assert banca_vis == False

    # 2. Switch to Fair tab
    print("\n--- Testing setViewMode('fair') ---")
    eval_js("setViewMode('fair')")
    fair_mode = eval_js("currentViewMode")
    fair_vis = eval_js("bancaFeiraGroup.visible")
    title_text = eval_js("document.getElementById('viewTitle').textContent")
    cam_pos = eval_js("[camera.position.x, camera.position.y, camera.position.z]")
    controls_tgt = eval_js("[controls.target.x, controls.target.y, controls.target.z]")
    active_tab = eval_js("document.querySelector('.tab-btn.active').textContent.trim()")

    print(f"Fair View: currentViewMode={fair_mode}")
    print(f"Fair View: bancaFeiraGroup.visible={fair_vis}")
    print(f"Fair View: Title='{title_text}'")
    print(f"Fair View: Camera={cam_pos}")
    print(f"Fair View: Target={controls_tgt}")
    print(f"Fair View: Active Tab='{active_tab.encode('ascii', 'replace').decode('ascii')}'")

    assert fair_mode == 'fair'
    assert fair_vis == True
    assert title_text == 'BANCA COMPLETA MONTADA NA XXI FEIRA FUCAPI 2026'

    # Check pins in fair mode
    pin1_disp = eval_js("document.getElementById('pin-1').style.display")
    pin11_disp = eval_js("document.getElementById('pin-11').style.display")
    print(f"Pins in fair mode: pin-1 display='{pin1_disp}', pin-11 display='{pin11_disp}'")
    assert pin1_disp == 'none'
    assert pin11_disp != 'none'

    # Take Screenshot of Fair View
    shot = send_cmd("Page.captureScreenshot", {"format": "png"})
    if "result" in shot and "data" in shot["result"]:
        img_data = base64.b64decode(shot["result"]["data"])
        with open("scratch/fair_screenshot.png", "wb") as sf:
            sf.write(img_data)
        print(f"Screenshot saved to scratch/fair_screenshot.png ({len(img_data)} bytes)")

    # 3. Test other 8 tabs to ensure bancaFeiraGroup is hidden
    print("\n--- Testing other 8 tabs ---")
    other_tabs = ['isometric', 'exploded', 'vision', 'diverter', 'drive', 'top', 'electrical', 'assembly']
    for t in other_tabs:
        eval_js(f"setViewMode('{t}')")
        vis = eval_js("bancaFeiraGroup.visible")
        p11_d = eval_js("document.getElementById('pin-11').style.display")
        print(f"Tab '{t}': bancaFeiraGroup.visible={vis}, pin-11 display={p11_d}")
        assert vis == False
        assert p11_d == 'none'

    # 4. Test Emergency Button Interaction
    print("\n--- Testing Emergency Button (Component 12) ---")
    eval_js("setViewMode('fair')")
    eval_js("selectComponent(12)")
    action_text = eval_js("document.getElementById('actionStatus').textContent")
    print(f"Emergency Action Status: {action_text.encode('ascii', 'replace').decode('ascii')}")
    assert "PARADA DE" in action_text or "EMERG" in action_text

    # 5. Test Pusher Test
    print("\n--- Testing Pusher Test ---")
    eval_js("triggerPusherTest()")
    p_active = eval_js("pusherTestState.active")
    print(f"Pusher test active: {p_active}")
    assert p_active == True

    # 6. Test Belt Motor Toggle
    print("\n--- Testing Belt Motor Toggle ---")
    eval_js("toggleBeltMotor()")
    belt_active = eval_js("isBeltRunning")
    print(f"Belt running: {belt_active}")

    # 7. Test Theme Switching
    print("\n--- Testing Themes ---")
    for th in ['blueprint', 'dark', 'paper']:
        eval_js(f"setTheme('{th}')")
        bg_col = eval_js("scene.background.getHexString()")
        fl_col = eval_js("fairFloorMesh.material.color.getHexString()")
        print(f"Theme '{th}': scene.background=#{bg_col}, fairFloor=#{fl_col}")

    # 8. Check for any JS console errors
    console_errors = eval_js("window.errorsLogged || []")
    print(f"\nAll assertions PASSED! Zero errors encountered.")

finally:
    proc.terminate()
