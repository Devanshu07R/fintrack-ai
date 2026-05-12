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

    # Sort months chronologically
    months = sorted(monthly.keys())

    values = [
        round(monthly[m], 2)
        for m in months
    ]

    return months, values


# ============================================
# 🤖 MONTHLY FORECAST MODEL
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

    # Features
    X = np.array(
        range(len(values))
    ).reshape(-1, 1)

    # Log scaling prevents huge spikes
    y = np.log1p(values)

    # Train model
    model = LinearRegression()
    model.fit(X, y)

    # Predict next month
    next_index = np.array(
        [[len(values)]]
    )

    pred_log = model.predict(next_index)[0]

    prediction = np.expm1(pred_log)

    # Smoothing
    avg = np.mean(values)

    prediction = (
        prediction * 0.7
        + avg * 0.3
    )

    # Prevent unrealistic predictions
    max_allowed = avg * 2.5

    prediction = min(
        prediction,
        max_allowed
    )

    # Trend logic
    if prediction > avg * 1.1:
        trend = "📈 Increasing spending"

    elif prediction < avg * 0.9:
        trend = "📉 Decreasing spending"

    else:
        trend = "📊 Stable spending"

    # Confidence
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

        "history":
            {
                "months": months,
                "values": values
            }
    }


# ============================================
# 📈 CATEGORY-WISE FORECAST
# ============================================

def category_prediction(expenses):

    category_data = defaultdict(list)

    # Group amounts category-wise
    for e in expenses:

        try:
            category_data[
                e.category
            ].append(float(e.amount))

        except:
            continue

    predictions = {}

    # Predict each category
    for cat, values in category_data.items():

        # Very little data
        if len(values) < 2:

            predictions[cat] = {

                "prediction":
                    round(sum(values), 2),

                "trend":
                    "Insufficient data"
            }

            continue

        # Features
        X = np.array(
            range(len(values))
        ).reshape(-1, 1)

        # Log transform
        y = np.log1p(values)

        model = LinearRegression()
        model.fit(X, y)

        pred_log = model.predict(
            [[len(values)]]
        )[0]

        prediction = np.expm1(pred_log)

        avg = np.mean(values)

        # Smoothing
        prediction = (
            prediction * 0.7
            + avg * 0.3
        )

        # Cap explosion
        prediction = min(
            prediction,
            avg * 2.5
        )

        # Trend
        if prediction > avg * 1.1:
            trend = "Increasing"

        elif prediction < avg * 0.9:
            trend = "Decreasing"

        else:
            trend = "Stable"

        predictions[cat] = {

            "prediction":
                round(float(prediction), 2),

            "average":
                round(float(avg), 2),

            "trend":
                trend
        }

    return predictions


# ============================================
# 🚨 SPIKE DETECTION
# ============================================

def detect_spending_spikes(expenses):

    _, values = prepare_monthly_data(
        expenses
    )

    if len(values) < 3:
        return []

    avg = np.mean(values)
    std = np.std(values)

    threshold = avg + (2 * std)

    spikes = []

    for i, value in enumerate(values):

        if value > threshold:

            spikes.append({

                "month_index": i,

                "amount":
                    round(float(value), 2),

                "issue":
                    "Unusual spending spike"
            })

    return spikes


# ============================================
# 💡 SAVINGS OPPORTUNITY ENGINE
# ============================================

def savings_opportunities(expenses):

    category_data = defaultdict(float)

    total = 0

    for e in expenses:

        try:
            amount = float(e.amount)

            category_data[e.category] += amount

            total += amount

        except:
            continue

    opportunities = []

    for cat, amount in category_data.items():

        percent = (
            amount / total * 100
        ) if total else 0

        if percent > 40:

            save_estimate = amount * 0.15

            opportunities.append({

                "category": cat,

                "spending_percent":
                    round(percent, 2),

                "potential_saving":
                    round(save_estimate, 2),

                "message":
                    f"Reduce {cat} spending "
                    f"to save approximately "
                    f"₹{round(save_estimate,2)}"
            })

    return opportunities


# ============================================
# 🤖 MASTER ML PREDICTOR
# ============================================

def ml_predictor_dashboard(expenses):

    monthly_forecast = predict_next_month(
        expenses
    )

    category_forecast = category_prediction(
        expenses
    )

    spikes = detect_spending_spikes(
        expenses
    )

    savings = savings_opportunities(
        expenses
    )

    return {

        "monthly_forecast":
            monthly_forecast,

        "category_forecast":
            category_forecast,

        "spending_spikes":
            spikes,

        "savings_opportunities":
            savings
    }