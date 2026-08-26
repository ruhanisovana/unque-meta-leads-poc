
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests, os
from datetime import datetime

app = Flask(__name__)
CORS(app)

leads_storage = []
PAGE_ACCESS_TOKEN = os.environ.get("PAGE_ACCESS_TOKEN", "")
VERIFY_TOKEN = "unque_verify_123"

@app.route("/")
def home():
    return jsonify({"status": "UnQue Live POC Running", "count": len(leads_storage)})

@app.route("/api/leads")
def get_leads():
    return jsonify({"leads": leads_storage[::-1]})

@app.route("/webhook", methods=["GET"])
def verify():
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.verify_token") == VERIFY_TOKEN:
        return request.args.get("hub.challenge"), 200
    return "Failed", 403

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    try:
        for entry in data.get("entry", []):
            for change in entry.get("changes", []):
                lead_id = change.get("value", {}).get("leadgen_id")
                if lead_id:
                    # Try fetch real lead
                    lead = None
                    if PAGE_ACCESS_TOKEN:
                        try:
                            r = requests.get(f"https://graph.facebook.com/v19.0/{lead_id}", params={"access_token": PAGE_ACCESS_TOKEN}, timeout=10)
                            if r.status_code == 200:
                                lead = r.json()
                        except: pass
                    if not lead:
                        lead = {
                            "id": lead_id,
                            "created_time": datetime.now().isoformat(),
                            "field_data": [
                                {"name": "full_name", "values": ["Test User from Meta Tool"]},
                                {"name": "email", "values": ["test@example.com"]}
                            ]
                        }
                    leads_storage.append(lead)
    except Exception as e:
        print(e)
    return "OK", 200

@app.route("/api/test-lead")
def test_lead():
    dummy = {
        "id": f"test_{len(leads_storage)+1}_{int(datetime.now().timestamp())}",
        "created_time": datetime.now().isoformat(),
        "field_data": [
            {"name": "full_name", "values": [f"Lead {len(leads_storage)+1}"]},
            {"name": "phone_number", "values": ["9876543210"]},
            {"name": "email", "values": [f"user{len(leads_storage)+1}@test.com"]}
        ]
    }
    leads_storage.append(dummy)
    return jsonify({"success": True, "lead": dummy})

@app.route("/api/clear")
def clear():
    leads_storage.clear()
    return jsonify({"cleared": True})
