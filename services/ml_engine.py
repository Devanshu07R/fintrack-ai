import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression


# ============================================
# 🧹 PREPARE DATAFRAME
# ============================================

def prepare_df(expenses):

    df = pd.DataFrame(expenses)

    if df.empty:
        return df

    # Safe conversions
    df["amount"] = pd.to_numeric(
        df["amount"],
        errors="coerce"
    )

    df["date"] = pd.to_datetime(
        df["date"],
        errors="coerce"
    )

    # Remove invalid rows
    df = df.dropna(subset=["amount", "date"])

    # Remove negative/zero invalid transactions
    df = df[df["amount"] > 0]

    # Sort by date
    df = df.sort_values("date")

    return df


# ============================================
# 📈 MONTHLY FORECAST ENGINE (FINAL)
# ============================================

def forecast(df):

    if len(df) < 3:
        return 0, "Not enough data"

    # ============================================
    # MONTHLY GROUPING
    # ============================================

    monthly = (
        df.groupby(
            df["date"].dt.to_period("M")
        )["amount"]
        .sum()
    )

    if len(monthly) < 2:
        return round(float(monthly.mean()), 2), "📊 Limited monthly data"

    monthly.index = monthly.index.astype(str)

    # ============================================
    # LOG SCALE
    # ============================================

    y = np.log1p(monthly.values)

    x = np.arange(len(y)).reshape(-1, 1)

    # ============================================
    # LINEAR REGRESSION
    # ============================================

    model = LinearRegression()
    model.fit(x, y)

    pred_log = model.predict(
        [[len(y)]]
    )[0]

    pred = np.expm1(pred_log)

    # ============================================
    # SMOOTHING
    # ============================================

    pred = (
        0.7 * pred
        + 0.3 * np.mean(monthly.values)
    )

    # ============================================
    # EXPLOSION PROTECTION
    # ============================================

    max_allowed = np.mean(
        monthly.values
    ) * 2

    pred = min(pred, max_allowed)

    avg_monthly = np.mean(monthly.values)

    # ============================================
    # TREND DETECTION
    # ============================================

    if pred > avg_monthly * 1.1:

        trend = "📈 Spending is increasing"

    elif pred < avg_monthly * 0.9:

        trend = "📉 Spending is decreasing"

    else:

        trend = "📊 Spending is stable"

    return round(float(pred), 2), trend


# ============================================
# 🚨 ANOMALY DETECTION
# ============================================

def detect_anomalies(df):

    if len(df) < 4:
        return []

    mean = df["amount"].mean()

    std = df["amount"].std()

    if std == 0:
        return []

    threshold = mean + (2 * std)

    anomalies = df[
        df["amount"] > threshold
    ]

    results = []

    for _, row in anomalies.iterrows():

        results.append({

            "amount":
                float(row["amount"]),

            "category":
                row["category"],

            "date":
                str(row["date"].date()),

            "issue":
                "Unusual high spending"
        })

    return results


# ============================================
# ⚠️ RISK SCORE ENGINE (FINAL)
# ============================================

def risk_score(df):

    if df.empty:
        return "LOW"

    mean = df["amount"].mean()

    if mean == 0:
        return "LOW"

    std = df["amount"].std()

    max_tx = df["amount"].max()

    cv = std / mean

    # ============================================
    # RISK LOGIC
    # ============================================

    if max_tx > mean * 6:

        return "HIGH"

    elif cv > 1.2:

        return "MEDIUM"

    return "LOW"


# ============================================
# 🧠 USER BEHAVIOR ANALYSIS
# ============================================

def behavior_cluster(df):

    if len(df) < 3:
        return "Normal spender"

    mean = df["amount"].mean()

    median = df["amount"].median()

    if median == 0:
        return "Normal spender"

    ratio = mean / median

    if ratio > 2.5:

        return "🚨 Extreme spending behavior"

    elif ratio > 1.5:

        return "⚠️ High spender segment"

    return "✅ Balanced spending pattern"


# ============================================
# 💳 CATEGORY ANALYSIS
# ============================================

def category_analysis(df):

    if df.empty:
        return {}

    category_totals = (

        df.groupby("category")["amount"]
        .sum()
        .sort_values(ascending=False)

    )

    total = category_totals.sum()

    result = {}

    for category, amount in category_totals.items():

        result[category] = {

            "amount":
                round(float(amount), 2),

            "percentage":
                round(
                    (amount / total) * 100,
                    2
                )
        }

    return result


# ============================================
# 🔄 RECURRING EXPENSE DETECTION
# ============================================

def recurring_expenses(df):

    if df.empty:
        return []

    recurring = []

    grouped = df.groupby("category")

    for category, data in grouped:

        if len(data) >= 3:

            avg = data["amount"].mean()

            std = data["amount"].std()

            if avg == 0:
                continue

            # Coefficient Variation
            cv = std / avg

            if cv < 0.2:

                recurring.append({

                    "category":
                        category,

                    "average_amount":
                        round(float(avg), 2),

                    "frequency":
                        len(data)
                })

    return recurring


# ============================================
# 💰 FINANCIAL HEALTH SCORE
# ============================================

def financial_health(
    df,
    anomalies,
    risk
):

    if df.empty:

        return {

            "score": 0,
            "status": "No data"
        }

    score = 100

    # ============================================
    # ANOMALY PENALTY
    # ============================================

    score -= min(
        len(anomalies) * 5,
        25
    )

    # ============================================
    # RISK PENALTY
    # ============================================

    if risk == "HIGH":

        score -= 30

    elif risk == "MEDIUM":

        score -= 15

    # ============================================
    # VOLATILITY PENALTY
    # ============================================

    mean = df["amount"].mean()

    std = df["amount"].std()

    if mean > 0:

        cv = std / mean

        if cv > 1.5:

            score -= 15

    # ============================================
    # BOUNDARIES
    # ============================================

    score = max(
        0,
        min(score, 100)
    )

    # ============================================
    # STATUS
    # ============================================

    if score >= 80:

        status = "Excellent"

    elif score >= 60:

        status = "Good"

    elif score >= 40:

        status = "Moderate"

    else:

        status = "Critical"

    return {

        "score": score,
        "status": status
    }


# ============================================
# 💡 SMART ADVISOR ENGINE
# ============================================

def advisor(
    df,
    risk,
    health
):

    if df.empty:

        return (
            "Add transactions "
            "to receive AI insights"
        )

    if risk == "HIGH":

        return (
            "🚨 Reduce high-value "
            "transactions immediately"
        )

    if health["score"] < 50:

        return (
            "⚠️ Your financial health "
            "needs attention"
        )

    if health["score"] > 80:

        return (
            "✅ Excellent financial "
            "management detected"
        )

    return (

        "📊 Spending is stable, "
        "but optimization is possible"

    )


# ============================================
# 🤖 MASTER AI ENGINE
# ============================================

def ai_insights(expenses):

    df = prepare_df(expenses)

    # ============================================
    # EMPTY STATE
    # ============================================

    if df.empty:

        return {

            "prediction": 0,

            "forecast": {

                "prediction": 0,
                "trend": "No data"

            },

            "anomalies": [],

            "risk": "LOW",

            "behavior":
                "No spending data",

            "advisor":
                "Add transactions",

            "financial_health": {

                "score": 0,
                "status": "No data"

            },

            "category_analysis": {},

            "recurring_expenses": []
        }

    # ============================================
    # CORE AI
    # ============================================

    pred, trend = forecast(df)

    anomalies = detect_anomalies(df)

    risk = risk_score(df)

    behavior = behavior_cluster(df)

    category_data = category_analysis(df)

    recurring = recurring_expenses(df)

    health = financial_health(
        df,
        anomalies,
        risk
    )

    advice = advisor(
        df,
        risk,
        health
    )

    # ============================================
    # FINAL AI RESPONSE
    # ============================================

    return {

        "prediction": pred,

        "forecast": {

            "prediction": pred,
            "trend": trend
        },

        "anomalies": anomalies,

        "risk": risk,

        "behavior": behavior,

        "advisor": advice,

        "financial_health":
            health,

        "category_analysis":
            category_data,

        "recurring_expenses":
            recurring
    }