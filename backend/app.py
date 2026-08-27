
from flask import Flask, request, jsonify
from datetime import datetime
import random

app = Flask(__name__)

# In-memory DB - This simulates Meta leads
leads_db = []

# 1. Meta Webhook Verification (for real tool) + Fake lead handling
@app.route('/api/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        # Meta will call this to verify
        if request.args.get('hub.verify_token') == 'unque123':
            return request.args.get('hub.challenge')
        return 'Forbidden', 403

    if request.method == 'POST':
        data = request.get_json()
        # This handles BOTH real Meta payload and our fake test-lead
        try:
            lead_id = data.get('entry', [{}])[0].get('changes', [{}])[0].get('value', {}).get('leadgen_id', 'fake_'+str(random.randint(1000,9999)))
            # Create lead like Meta does
            new_lead = {
                "id": lead_id,
                "created_time": datetime.now().isoformat(),
                "field_data": [
                    {"name": "full_name", "values": [f"Test User {random.randint(1,100)}"]},
                    {"name": "phone_number", "values": [f"+91 98{random.randint(10000000,99999999)}"]},
                    {"name": "email", "values": [f"test{random.randint(1,1000)}@example.com"]}
                ]
            }
            leads_db.insert(0, new_lead)
        except:
            pass
        return 'EVENT_RECEIVED', 200

# 2. Get all leads - App calls this every 2 sec
@app.route('/api/leads', methods=['GET'])
def get_leads():
    return jsonify({"count": len(leads_db), "leads": leads_db})

# 3. Fake Meta Lead Testing Tool - THIS IS YOUR BLUE BUTTON
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
    leads_db.insert(0, new_lead)
    return jsonify({"success": True, "lead": new_lead, "count": len(leads_db)})

@app.route('/', methods=['GET'])
def home():
    return jsonify({"status": "UnQue PoC Running", "total_leads": len(leads_db)})
