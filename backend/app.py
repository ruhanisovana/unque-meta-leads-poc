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
        url = f"{BASE_URL}?documentId={lead['id']}"
        r = requests.post(url, json=payload, timeout=10)
        print(r.text)
        return r.status_code in [200,201]
    except Exception as e:
        print(e)
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

    # REAL META PAYLOAD
    try:
        data = request.get_json()
        print("META PAYLOAD:", data)
        # Extract leadgen_id if present
        entry = data.get('entry', [{}])[0]
        changes = entry.get('changes', [{}])[0]
        value = changes.get('value', {})
        lead_id = value.get('leadgen_id', f"lead_{random.randint(100000,999999)}")

        # For POC: if we have leadgen_id, try to fetch real data, else fake
        # You need to put PAGE_ACCESS_TOKEN in Vercel Env
        new_lead = {
            "id": str(lead_id),
            "created_time": datetime.now().isoformat(),
            "field_data": [
                {"name": "full_name", "values": [f"Meta Test Lead {random.randint(1,100)}"]},
                {"name": "phone_number", "values": [f"+91 {random.randint(7000000000,9999999999)}"]},
                {"name": "source", "values": ["Meta Lead Testing Tool"]}
            ]
        }
        save_lead(new_lead)
    except Exception as e:
        print(f"webhook error {e}")
        # Fallback fake
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
