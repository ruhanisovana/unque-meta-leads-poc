from flask import Flask, request, jsonify
from datetime import datetime
import random, json, requests

app = Flask(__name__)
application = app
handler = app

PROJECT_ID = "unque-3c9d1"
BASE_URL = f"https://firestore.googleapis.com/v1/projects/{PROJECT_ID}/databases/(default)/documents/leads"

def get_leads():
    try:
        r = requests.get(BASE_URL, timeout=10)
        if r.status_code == 200:
            docs = r.json().get('documents', [])
            leads = []
            for d in docs:
                fid = d['name'].split('/')[-1]
                f = d.get('fields', {})
                # Try to get any name/phone
                name = f.get('name', {}).get('stringValue') or f.get('full_name', {}).get('stringValue') or "Unknown"
                phone = f.get('phone', {}).get('stringValue') or f.get('phone_number', {}).get('stringValue') or ""
                # Check if field_data exists (from webhook)
                fd_raw = f.get('field_data', {}).get('stringValue')
                if fd_raw:
                    try:
                        fd = json.loads(fd_raw)
                    except:
                        fd = [{"name":"full_name","values":[name]}, {"name":"phone","values":[phone]}]
                else:
                    fd = [{"name":"full_name","values":[name]}, {"name":"phone","values":[phone]}]
                leads.append({"id": fid, "field_data": fd, "raw": f})
            return leads
        elif r.status_code == 404:
            return [] # No collection yet
    except Exception as e:
        print(e)
    return []

def save_lead(lead):
    try:
        payload = {
            "fields": {
                "created_time": {"stringValue": lead['created_time']},
                "field_data": {"stringValue": json.dumps(lead['field_data'])}
            }
        }
        url = f"{BASE_URL}/{lead['id']}"
        requests.patch(url, json=payload, timeout=10)
        return True
    except:
        return False

@app.route('/', methods=['GET'])
def home():
    leads = get_leads()
    return jsonify({"status": "UnQue FINAL", "total_leads": len(leads), "leads": leads})

@app.route('/api/leads', methods=['GET'])
def leads_route():
    leads = get_leads()
    return jsonify({"count": len(leads), "leads": leads})

@app.route('/api/test-lead', methods=['GET','POST'])
def test_lead():
    new_lead = {
        "id": f"lead_{random.randint(100000,999999)}",
        "created_time": datetime.now().isoformat(),
        "field_data": [
            {"name": "full_name", "values": [f"Fake Lead {random.randint(1,100)}"]},
            {"name": "phone_number", "values": [f"+91 98765{random.randint(10000,99999)}"]}
        ]
    }
    save_lead(new_lead)
    return jsonify({"success": True, "count": len(get_leads())})

@app.route('/api/webhook', methods=['GET','POST'])
def webhook():
    if request.method == 'GET':
        if request.args.get('hub.verify_token') == 'unque123':
            return request.args.get('hub.challenge')
        return 'Forbidden', 403
    new_lead = {
        "id": f"lead_{random.randint(100000,999999)}",
        "created_time": datetime.now().isoformat(),
        "field_data": [
            {"name": "full_name", "values": [f"Meta User {random.randint(1,100)}"]},
            {"name": "phone_number", "values": [f"+91 98{random.randint(10000000,99999999)}"]}
        ]
    }
    save_lead(new_lead)
    return 'EVENT_RECEIVED', 200
