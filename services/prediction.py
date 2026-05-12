import numpy as np
from sklearn.linear_model import LinearRegression
from collections import defaultdict
from datetime import datetime


# ============================================
# 📊 PREPARE MONTHLY DATA
# ============================================

def prepare_monthly_data(expenses):

    monthly = defaultdict(float)

    for e in expenses:

        if not e.date:
            continue

        try:
            # Safe date parsing
            date_obj = datetime.strptime(
                str(e.date)[:10],
                "%Y-%m-%d"
            )

            month = date_obj.strftime("%Y-%m")

            monthly[month] += float(e.amount)

        except:
            continue

    # Sort months properly
    sorted_months = sorted(monthly.keys())

    values = [
        monthly[m]
        for m in sorted_months
    ]

    return sorted_months, values


# ============================================
# 🤖 PREDICT NEXT MONTH SPENDING
# ============================================

def predict_next_month(expenses):

    months, values = prepare_monthly_data(
        expenses
    )

    # Not enough data
    if len(values) < 2:

        return {
            "prediction": 0,
            "trend": "Not enough data",
            "confidence": "LOW"
        }

    # X axis
    X = np.array(
        range(len(values))
    ).reshape(-1, 1)

    # Log scaling prevents huge jumps
    y = np.log1p(values)

    # Train ML model
    model = LinearRegression()
    model.fit(X, y)

    # Predict next month
    next_month_index = np.array(
        [[len(values)]]
    )

    pred_log = model.predict(
        next_month_index
    )[0]

    prediction = np.expm1(pred_log)

    # Smooth prediction
    avg = np.mean(values)

    prediction = (
        prediction * 0.7
        + avg * 0.3
    )

    # Prevent unrealistic spikes
    prediction = min(
        prediction,
        avg * 2.5
    )

    # Trend analysis
    if prediction > avg * 1.1:
        trend = "📈 Spending increasing"

    elif prediction < avg * 0.9:
        trend = "📉 Spending decreasing"

    else:
        trend = "📊 Stable spending"

    # Confidence level
    std = np.std(values)

    cv = std / (avg + 1)

    if cv < 0.3:
        confidence = "HIGH"

    elif cv < 0.7:
        confidence = "MEDIUM"

    else:
        confidence = "LOW"

    return {

        "prediction":
            round(float(prediction), 2),

        "trend":
            trend,

        "confidence":
            confidence,

        "history": {
            "months": months,
            "values": values
        }
    }


# ============================================
# 📉 SPENDING INSIGHT ENGINE
# ============================================

def spending_insight(expenses):

    if len(expenses) < 3:

        return {
            "status": "INFO",
            "message":
                "Not enough data for insights"
        }

    amounts = []

    for e in expenses:

        try:
            amounts.append(
                float(e.amount)
            )

        except:
            continue

    if not amounts:

        return {
            "status": "INFO",
            "message":
                "No valid expense data"
        }

    total = sum(amounts)

    avg = total / len(amounts)

    std = np.std(amounts)

    # Dynamic anomaly threshold
    threshold = avg + (1.5 * std)

    high_spending = [

        amt for amt in amounts

        if amt > threshold
    ]

    # High overspending detection
    if len(high_spending) >= 3:

        return {

            "status": "WARNING",

            "message":
                "⚠️ Frequent high-value "
                "transactions detected",

            "average":
                round(avg, 2),

            "spikes":
                len(high_spending)
        }

    # Stable behavior
    if std < avg * 0.4:

        return {

            "status": "GOOD",

            "message":
                "✅ Spending pattern "
                "is stable",

            "average":
                round(avg, 2)
        }

    # Moderate variation
    return {

        "status": "MEDIUM",

        "message":
            "📊 Moderate spending "
            "variation detected",

        "average":
            round(avg, 2)
    }


# ============================================
# 📈 CATEGORY-WISE ANALYSIS
# ============================================

def category_analysis(expenses):

    category_totals = defaultdict(float)

    total = 0

    for e in expenses:

        try:

            amount = float(e.amount)

            category_totals[
                e.category
            ] += amount

            total += amount

        except:
            continue

    result = []

    for category, amount in category_totals.items():

        percent = (
            amount / total * 100
        ) if total else 0

        result.append({

            "category":
                category,

            "amount":
                round(amount, 2),

            "percentage":
                round(percent, 2)
        })

    # Sort highest spending first
    result.sort(
        key=lambda x: x["amount"],
        reverse=True
    )

    return result


# ============================================
# 🚨 ANOMALY DETECTION
# ============================================

def detect_anomalies(expenses):

    amounts = []

    valid_expenses = []

    for e in expenses:

        try:

            amount = float(e.amount)

            amounts.append(amount)

            valid_expenses.append(e)

        except:
            continue

    if len(amounts) < 4:
        return []

    mean = np.mean(amounts)

    std = np.std(amounts)

    threshold = mean + (2 * std)

    anomalies = []

    for e in valid_expenses:

        amount = float(e.amount)

        if amount > threshold:

            anomalies.append({

                "amount":
                    amount,

                "category":
                    e.category,

                "date":
                    str(e.date),

                "issue":
                    "Unusual spending spike"
            })

    return anomalies


# ============================================
# 💡 MASTER PREDICTION ENGINE
# ============================================

def prediction_dashboard(expenses):

    return {

        "forecast":
            predict_next_month(
                expenses
            ),

        "insight":
            spending_insight(
                expenses
            ),

        "categories":
            category_analysis(
                expenses
            ),

        "anomalies":
            detect_anomalies(
                expenses
            )
    }