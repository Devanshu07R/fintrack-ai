from flask import Blueprint, jsonify
from models.expense import Expense
from services.ml_engine import ai_insights

ai_bp = Blueprint("ai", __name__)

@ai_bp.route("/dashboard", methods=["GET"])
def ai_dashboard():

    expenses = Expense.query.all()

    data = [
        {
            "amount": e.amount,
            "category": e.category,
            "date": str(e.date)
        }
        for e in expenses
    ]

    insights = ai_insights(data)

    return jsonify({
        "prediction": insights.get("prediction", 0),

        "forecast": {
            "prediction": insights.get("forecast", {}).get("prediction", 0),
            "trend": insights.get("forecast", {}).get("trend", "No trend")
        },

        "anomalies": insights.get("anomalies", []),
        "risk": insights.get("risk", "LOW"),
        "behavior": insights.get("behavior", ""),
        "advisor": insights.get("advisor", "AI active")
    })