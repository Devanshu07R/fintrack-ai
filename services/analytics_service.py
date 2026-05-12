from flask import Blueprint, jsonify
from services.analytics import (
    total_spent,
    category_breakdown
)

from services.analytics_engine import (
    monthly_trend,
    detect_anomalies,
    burn_rate,
    smart_insights
)

from services.ai_intelligence import (
    generate_ai_report
)

from services.alert_service import (
    budget_alert
)

from models.expense_model import Expense


analytics_bp = Blueprint("analytics", __name__)


# ==========================================
# 📊 BASIC SUMMARY API
# ==========================================
@analytics_bp.route("/summary", methods=["GET"])
def summary():

    expenses = Expense.query.all()

    total = total_spent()
    category_data = category_breakdown()

    return jsonify({
        "success": True,

        "total_spent": total,

        "transaction_count": len(expenses),

        "category_breakdown": category_data,

        "budget_status": budget_alert(
            total,
            50000
        )
    })


# ==========================================
# 🤖 COMPLETE AI DASHBOARD API
# ==========================================
@analytics_bp.route("/ai-dashboard", methods=["GET"])
def ai_dashboard():

    expenses = Expense.query.all()

    total = sum(
        float(e.amount or 0)
        for e in expenses
    )

    ai_report = generate_ai_report(expenses)

    analytics = {
        "monthly_trend": monthly_trend(expenses),

        "anomalies": detect_anomalies(expenses),

        "burn_rate": burn_rate(
            expenses,
            monthly_budget=50000
        ),

        "smart_insights": smart_insights(expenses)
    }

    return jsonify({

        "success": True,

        # =========================
        # BASIC STATS
        # =========================
        "overview": {
            "total_spent": round(total, 2),

            "transactions": len(expenses),

            "budget_alert": budget_alert(
                total,
                50000
            )
        },

        # =========================
        # AI ENGINE
        # =========================
        "ai_report": ai_report,

        # =========================
        # ANALYTICS ENGINE
        # =========================
        "analytics": analytics
    })


# ==========================================
# 🚨 ANOMALIES API
# ==========================================
@analytics_bp.route("/anomalies", methods=["GET"])
def anomalies():

    expenses = Expense.query.all()

    return jsonify({
        "success": True,

        "count": len(
            detect_anomalies(expenses)
        ),

        "data": detect_anomalies(expenses)
    })


# ==========================================
# 📈 MONTHLY TREND API
# ==========================================
@analytics_bp.route("/trend", methods=["GET"])
def trend():

    expenses = Expense.query.all()

    return jsonify({
        "success": True,

        "data": monthly_trend(expenses)
    })


# ==========================================
# 🔥 BURN RATE API
# ==========================================
@analytics_bp.route("/burn-rate", methods=["GET"])
def burnrate():

    expenses = Expense.query.all()

    return jsonify({
        "success": True,

        "data": burn_rate(
            expenses,
            monthly_budget=50000
        )
    })


# ==========================================
# 💡 SMART INSIGHTS API
# ==========================================
@analytics_bp.route("/insights", methods=["GET"])
def insights():

    expenses = Expense.query.all()

    return jsonify({
        "success": True,

        "data": smart_insights(expenses)
    })


# ==========================================
# 🧠 FULL SYSTEM HEALTH API
# ==========================================
@analytics_bp.route("/system-health", methods=["GET"])
def system_health():

    expenses = Expense.query.all()

    total = sum(
        float(e.amount or 0)
        for e in expenses
    )

    risk = "LOW"

    if total > 30000:
        risk = "MEDIUM"

    if total > 50000:
        risk = "HIGH"

    return jsonify({

        "success": True,

        "system_status": "ACTIVE",

        "risk_level": risk,

        "records_processed": len(expenses),

        "ai_engine": "ONLINE",

        "analytics_engine": "RUNNING"
    })