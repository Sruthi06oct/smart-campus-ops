from flask import Blueprint, request, jsonify
from rag_engine import retrieve, load_pdf
from alert_service import add_alert, get_alerts
from analytics import log_query, stats
import os

routes = Blueprint("routes", __name__)
os.makedirs("uploads", exist_ok=True)

@routes.route("/upload", methods=["POST"])
def upload():
    f = request.files["file"]
    path = os.path.join("uploads", f.filename)
    f.save(path)
    load_pdf(path)
    return jsonify({"message": "PDF processed"})

@routes.route("/ask", methods=["POST"])
def ask():
    q = request.json["question"]
    log_query(q)
    return jsonify({"answer": "\n".join(retrieve(q))})

@routes.route("/alert", methods=["POST"])
def alert():
    add_alert(request.json["message"])
    return jsonify({"status": "ok"})

@routes.route("/alerts", methods=["GET"])
def alerts():
    return jsonify(get_alerts())

@routes.route("/stats", methods=["GET"])
def statistics():
    return jsonify(stats())
