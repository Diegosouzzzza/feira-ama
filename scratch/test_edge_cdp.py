import subprocess
import time
import json
import urllib.request

edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
file_url = r"file:///C:/Users/ponto/OneDrive/Desktop/FEIRA%20-%20AMA/Manual_Montagem_Esteira_70cm.html"

# Launch Edge headless with remote debugging
proc = subprocess.Popen([
    edge_path,
    "--headless=new",
    "--remote-debugging-port=9222",
    "--allow-file-access-from-files",
    file_url
])

try:
    time.sleep(2)
    # Check if CDP is responding
    resp = urllib.request.urlopen("http://127.0.0.1:9222/json")
    targets = json.loads(resp.read().decode())
    print("Edge targets:", len(targets))
    for t in targets:
        print(t.get("title"), t.get("url"))
finally:
    proc.terminate()
