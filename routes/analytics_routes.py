from flask import Blueprint, jsonify
from models.expense import Expense
from services.analytics_engine import (
    monthly_trend,
    detect_anomalies,
    burn_rate,
    smart_insights
)

analytics_bp = Blueprint("analytics", __name__)


# =========================
# 📊 FULL ANALYTICS DASHBOARD API
# =========================
@analytics_bp.route("/summary", methods=["GET"])
def summary():
    expenses = Expense.query.all()

    return jsonify({
        "trend": monthly_trend(expenses),
        "anomalies": detect_anomalies(expenses),
        "burn_rate": burn_rate(expenses),
        "insights": smart_insights(expenses)
    })