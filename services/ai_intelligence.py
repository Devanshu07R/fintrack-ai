from collections import defaultdict
from datetime import datetime
import numpy as np


# ==========================================
# 🔥 HELPER FUNCTIONS
# ==========================================

def safe_float(value):
    try:
        return float(value)
    except:
        return 0.0


def sort_expenses_by_date(expenses):
    try:
        return sorted(
            expenses,
            key=lambda x: datetime.strptime(
                str(x.date).split(" ")[0],
                "%Y-%m-%d"
            )
        )
    except:
        return expenses


# ==========================================
# ⚠️ 1. ADVANCED ANOMALY DETECTION
# ==========================================

def detect_anomalies(expenses):

    anomalies = []

    category_values = defaultdict(list)

    # GROUP CATEGORY VALUES
    for e in expenses:
        category_values[e.category].append(
            safe_float(e.amount)
        )

    # DETECT SPIKES
    for cat, values in category_values.items():

        if len(values) < 2:
            continue

        avg = np.mean(values)
        std = np.std(values)

        for v in values:

            # Z-SCORE LIKE DETECTION
            if std > 0 and v > (avg + 2 * std):

                anomalies.append({
                    "category": cat,
                    "amount": round(v, 2),
                    "reason": "Unusual spending spike detected"
                })

    return anomalies


# ==========================================
# 📈 2. REAL SPENDING TREND ANALYSIS
# ==========================================

def spending_trend(expenses):

    if len(expenses) < 3:
        return {
            "trend": "Not enough data",
            "slope": 0
        }

    # SORT BY DATE
    expenses = sort_expenses_by_date(expenses)

    amounts = [
        safe_float(e.amount)
        for e in expenses
    ]

    x = np.arange(len(amounts))

    # LINEAR REGRESSION SLOPE
    slope = np.polyfit(x, amounts, 1)[0]

    if slope > 1000:
        trend_text = "📈 Spending is increasing"
    elif slope < -1000:
        trend_text = "📉 Spending is decreasing"
    else:
        trend_text = "📊 Stable spending pattern"

    return {
        "trend": trend_text,
        "slope": round(float(slope), 2)
    }


# ==========================================
# 🧠 3. USER BEHAVIOR ANALYSIS
# ==========================================

def behavior_analysis(expenses):

    category_total = defaultdict(float)

    for e in expenses:
        category_total[e.category] += safe_float(e.amount)

    total = sum(category_total.values())

    insights = []

    if total == 0:
        return ["No spending data available"]

    # CATEGORY DOMINANCE
    for cat, value in category_total.items():

        percent = (value / total) * 100

        if percent >= 50:
            insights.append(
                f"⚠️ Heavy spending on {cat} ({round(percent)}%)"
            )

        elif percent >= 30:
            insights.append(
                f"📌 Major spending category: {cat} ({round(percent)}%)"
            )

    # LOW CATEGORY DIVERSITY
    if len(category_total) <= 2:
        insights.append(
            "⚠️ Spending categories are not diversified"
        )

    # HIGH EXPENSE USER
    if total > 500000:
        insights.append(
            "💰 High overall spending behavior detected"
        )

    return insights


# ==========================================
# 💡 4. SMART ADVISOR ENGINE
# ==========================================

def smart_advisor(expenses):

    total = sum(
        safe_float(e.amount)
        for e in expenses
    )

    advice = []

    # TOTAL SPENDING ANALYSIS
    if total > 1000000:
        advice.append(
            "🚨 Critical spending level detected"
        )

    elif total > 500000:
        advice.append(
            "⚠️ Optimize discretionary spending"
        )

    elif total > 100000:
        advice.append(
            "💡 Consider setting stricter monthly limits"
        )

    else:
        advice.append(
            "✅ Spending habits look healthy"
        )

    # AVERAGE TRANSACTION
    if len(expenses) > 0:

        avg = total / len(expenses)

        advice.append(
            f"📊 Average transaction value: ₹{round(avg)}"
        )

    # LARGE SINGLE TRANSACTION
    max_transaction = max(
        [safe_float(e.amount) for e in expenses],
        default=0
    )

    if max_transaction > 300000:
        advice.append(
            "🔥 Large individual transaction detected"
        )

    return advice


# ==========================================
# 🔥 5. FINANCIAL RISK ENGINE
# ==========================================

def risk_analysis(expenses):

    total = sum(
        safe_float(e.amount)
        for e in expenses
    )

    if total > 1000000:
        return "HIGH"

    elif total > 300000:
        return "MEDIUM"

    return "LOW"


# ==========================================
# 🔮 6. AI EXPENSE PREDICTION
# ==========================================

def predict_next_month(expenses):

    if len(expenses) < 2:
        return 0

    expenses = sort_expenses_by_date(expenses)

    amounts = [
        safe_float(e.amount)
        for e in expenses
    ]

    x = np.arange(len(amounts))

    slope, intercept = np.polyfit(x, amounts, 1)

    next_index = len(amounts)

    prediction = slope * next_index + intercept

    return round(max(prediction, 0), 2)


# ==========================================
# 🚀 7. MASTER AI REPORT
# ==========================================

def generate_ai_report(expenses):

    trend_data = spending_trend(expenses)

    advisor = smart_advisor(expenses)

    return {

        "prediction": predict_next_month(expenses),

        "forecast": {
            "trend": trend_data["trend"],
            "slope": trend_data["slope"]
        },

        "risk": risk_analysis(expenses),

        "advisor": advisor[0] if advisor else "No advice",

        "advisor_list": advisor,

        "behavior": behavior_analysis(expenses),

        "anomalies": detect_anomalies(expenses)
    }