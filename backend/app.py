from flask import Flask, request, jsonify
from datetime import datetime
import random, os, json

app = Flask(__name__)

# Try Firebase
db = None
try:
    import firebase_admin
    from firebase_admin import credentials, firestore
    if not firebase_admin._apps:
        # Use project id from env
        firebase_admin.initialize_app(options={'projectId': os.getenv('NEXT_PUBLIC_FIREBASE_PROJECT_ID') or os.getenv('FIREBASE_PROJECT_ID') or 'unque-3c9d1'})
    db = firestore.client()
    print("Firebase connected")
except Exception as e:
    print(f"Firebase failed: {e}, using tmp fallback")
    db = None

TMP_FILE = '/tmp/leads.json'

def get_leads():
    if db:
        try:
            docs = db.collection('leads').order_by('created_time', direction=firestore.Query.DESCENDING).limit(50).stream()
            leads = [doc.to_dict() for doc in docs]
            return leads
        except Exception as e:
            print(f"Firestore get error: {e}")
    
    if os.path.exists(TMP_FILE):
        try:
            with open(TMP_FILE, 'r') as f:
                return json.load(f)
        except:
            return []
    return []

def save_lead(lead):
    if db:
        try:
            db.collection('leads').document(lead['id']).set(lead)
            return
        except Exception as e:
            print(f"Firestore save error: {e}")
    
    leads = get_leads()
    leads.insert(0, lead)
    with open(TMP_FILE, 'w') as f:
        json.dump(leads, f)

@app.route('/api/webhook', methods=['GET', 'POST'])
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

@app.route('/api/leads', methods=['GET'])
def get_leads_route():
    leads = get_leads()
    return jsonify({"count": len(leads), "leads": leads})

@app.route('/api/test-lead', methods=['GET', 'POST'])
def test_lead():
    new_lead = {
        "id": f"lead_{random.randint(100000,999999)}",
        "created_time": datetime.now().isoformat(),
        "field_data": [
            {"name": "full_name", "values": [f"Fake Lead {random.randint(1,100)}"]},
            {"name": "phone_number", "values": [f"+91 98765{random.randint(10000,99999)}"]},
            {"name": "email", "values": [f"fake{random.randint(1,999)}@test.com"]}
        ]
    }
    save_lead(new_lead)
    leads = get_leads()
    return jsonify({"success": True, "count": len(leads), "lead": new_lead, "leads": leads})

@app.route('/', methods=['GET'])
def home():
    leads = get_leads()
    return jsonify({"status": "UnQue PoC Running - FIXED", "total_leads": len(leads)})
