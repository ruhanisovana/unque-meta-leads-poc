from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return jsonify({
        "status": "ok",
        "message": "UnQue Meta Leads backend is running"
    })

@app.route("/health")
def health():
    return jsonify({
        "status": "healthy"
    })

@app.route("/api/leads", methods=["POST", "GET"])
def leads():
    return jsonify({"success": True, "message": "Leads endpoint ready - connect Supabase here"})

