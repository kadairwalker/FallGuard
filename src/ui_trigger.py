import json
import time
import urllib.request
 
FIREBASE_URL = "https://fallguard-demo-default-rtdb.firebaseio.com/fallguard_trigger.json"
 
 
def trigger_ui_alert():
    try:
        payload = json.dumps({"ts": time.time(), "source": "raspberry_pi"}).encode("utf-8")
        req = urllib.request.Request(FIREBASE_URL, data=payload, method="PUT")
        req.add_header("Content-Type", "application/json")
        urllib.request.urlopen(req, timeout=3)
    except Exception as e:
        print(f"    (couldn't reach UI: {e})")
