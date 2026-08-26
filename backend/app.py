from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

VERIFY_TOKEN = "unque123"

leads_storage = []

@app.route("/")
def home():
    return jsonify({"status": "ok", "message": "UnQue Meta Leads backend is running"})

@app.route("/health")
def health():
    return jsonify({"status": "healthy"})

# Meta will call this to verify webhook
@app.route("/webhook", methods=["GET"])
def verify():
    if request.args.get("hub.verify_token") == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return "Verification failed", 403

# Meta will send leads here
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    leads_storage.append(data)
    print("New Lead:", data)
    return jsonify({"success": True}), 200

@app.route("/api/leads", methods=["GET"])
def get_leads():
    return jsonify({"success": True, "leads": leads_storage, "count": len(leads_storage)})

@app.route("/api/leads", methods=["POST"])
def add_lead():
    lead = request.get_json()
    leads_storage.append(lead)
    return jsonify({"success": True, "leads": leads_storage})
