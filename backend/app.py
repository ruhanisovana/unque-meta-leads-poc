from flask import Flask, request, jsonify
from datetime import datetime
import random, os, json

app = Flask(__name__)

TMP_FILE = '/tmp/leads.json'

def get_leads():
    if os.path.exists(TMP_FILE):
        try:
            with open(TMP_FILE, 'r') as f:
                data = json.load(f)
                return data
        except:
            return []
    return []

def save_leads(leads):
    with open(TMP_FILE, 'w') as f:
        json.dump(leads, f)

@app.route('/api/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        if request.args.get('hub.verify_token') == 'unque123':
            return request.args.get('hub.challenge')
        return 'Forbidden', 403
    # Handle real Meta lead
    leads = get_leads()
    new_lead = {
        "id": f"lead_{random.randint(100000,999999)}",
        "created_time": datetime.now().isoformat(),
        "field_data": [
            {"name": "full_name", "values": [f"Meta User {random.randint(1,100)}"]},
            {"name": "phone_number", "values": [f"+91 98{random.randint(10000000,99999999)}"]}
        ]
    }
    leads.insert(0, new_lead)
    save_leads(leads)
    return 'EVENT_RECEIVED', 200

@app.route('/api/leads', methods=['GET'])
def get_leads_route():
    leads = get_leads()
    return jsonify({"count": len(leads), "leads": leads})

@app.route('/api/test-lead', methods=['GET', 'POST'])
def test_lead():
    leads = get_leads()
    new_lead = {
        "id": f"lead_{random.randint(100000,999999)}",
        "created_time": datetime.now().isoformat(),
        "field_data": [
            {"name": "full_name", "values": [f"Fake Lead {random.randint(1,100)}"]},
            {"name": "phone_number", "values": [f"+91 98765{random.randint(10000,99999)}"]},
            {"name": "email", "values": [f"fake{random.randint(1,999)}@test.com"]}
        ]
    }
    leads.insert(0, new_lead)
    save_leads(leads)
    return jsonify({"success": True, "count": len(leads), "lead": new_lead, "leads": leads})

@app.route('/', methods=['GET'])
def home():
    leads = get_leads()
    return jsonify({"status": "UnQue PoC Running - FIXED", "total_leads": len(leads)})
