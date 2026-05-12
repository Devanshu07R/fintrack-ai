from collections import defaultdict
from datetime import datetime
import statistics

# =========================================================
# 📊 1. MONTHLY TREND ANALYSIS
# =========================================================
def monthly_trend(expenses):

    monthly = defaultdict(float)

    for e in expenses:

        if not e.date:
            continue

        try:
            # Handles:
            # 2026-05-11
            # 2026-05-11 00:00:00
            parsed_date = datetime.strptime(
                str(e.date).split(" ")[0],
                "%Y-%m-%d"
            )

            month = parsed_date.strftime("%Y-%m")

            monthly[month] += float(e.amount)

        except Exception:
            continue

    # If no data
    if not monthly:
        return []

    sorted_months = sorted(monthly.keys())

    trend = []

    for i in range(len(sorted_months)):

        month = sorted_months[i]
        current_spend = monthly[month]

        growth = 0

        if i > 0:
            prev_spend = monthly[sorted_months[i - 1]]

            if prev_spend != 0:
                growth = (
                    (current_spend - prev_spend)
                    / prev_spend
                ) * 100

        trend.append({
            "month": month,
            "spent": round(current_spend, 2),
            "growth_percent": round(growth, 2)
        })

    return trend


# =========================================================
# ⚠️ 2. SMART ANOMALY DETECTION
# =========================================================
def detect_anomalies(expenses):

    anomalies = []

    if len(expenses) < 3:
        return anomalies

    category_map = defaultdict(list)

    # Group by category
    for e in expenses:

        try:
            amount = float(e.amount)

            category_map[e.category].append({
                "amount": amount,
                "date": e.date
            })

        except Exception:
            continue

    # Detect anomalies using statistics
    for category, values in category_map.items():

        amounts = [v["amount"] for v in values]

        if len(amounts) < 3:
            continue

        avg = statistics.mean(amounts)

        try:
            std = statistics.stdev(amounts)
        except Exception:
            std = 0

        threshold = avg + (2 * std)

        for item in values:

            if item["amount"] > threshold:

                anomalies.append({
                    "category": category,
                    "amount": round(item["amount"], 2),
                    "date": item["date"],
                    "issue": "Unusual spending spike detected"
                })

    return anomalies


# =========================================================
# 💰 3. ADVANCED BURN RATE ANALYSIS
# =========================================================
def burn_rate(expenses, monthly_budget=30000):

    if not expenses:
        return {
            "daily_spend": 0,
            "expected_month": 0,
            "budget_usage_percent": 0,
            "status": "No data"
        }

    total = 0
    unique_days = set()

    for e in expenses:

        try:
            total += float(e.amount)

            if e.date:
                day = str(e.date).split(" ")[0]
                unique_days.add(day)

        except Exception:
            continue

    active_days = len(unique_days)

    if active_days == 0:
        active_days = 1

    daily_spend = total / active_days

    expected_month = daily_spend * 30

    budget_percent = (
        (expected_month / monthly_budget) * 100
        if monthly_budget > 0 else 0
    )

    # Smart status
    if budget_percent >= 120:
        status = "Critical Overspending"

    elif budget_percent >= 100:
        status = "Overspending Risk"

    elif budget_percent >= 80:
        status = "Warning Zone"

    else:
        status = "Healthy"

    return {
        "daily_spend": round(daily_spend, 2),
        "expected_month": round(expected_month, 2),
        "budget_usage_percent": round(budget_percent, 2),
        "status": status
    }


# =========================================================
# 💡 4. SMART INSIGHTS ENGINE
# =========================================================
def smart_insights(expenses):

    if not expenses:
        return [
            "No financial data available yet"
        ]

    insights = []

    total = sum(
        float(e.amount)
        for e in expenses
    )

    avg = total / len(expenses)

    # -----------------------------------------
    # High Spending Frequency
    # -----------------------------------------
    high_spends = [
        e for e in expenses
        if float(e.amount) > avg * 1.5
    ]

    if len(high_spends) >= 3:
        insights.append(
            "⚠️ Frequent high-value transactions detected"
        )

    # -----------------------------------------
    # Category Analysis
    # -----------------------------------------
    category_totals = defaultdict(float)

    for e in expenses:
        category_totals[e.category] += float(e.amount)

    top_category = max(
        category_totals,
        key=category_totals.get
    )

    top_percent = (
        category_totals[top_category]
        / total
    ) * 100

    insights.append(
        f"📊 Highest spending category: "
        f"{top_category} "
        f"({round(top_percent, 1)}%)"
    )

    # -----------------------------------------
    # Diversity Analysis
    # -----------------------------------------
    unique_categories = len(category_totals)

    if unique_categories < 3:
        insights.append(
            "⚠️ Low spending diversity observed"
        )

    elif unique_categories >= 5:
        insights.append(
            "✅ Healthy spending diversification"
        )

    # -----------------------------------------
    # Savings Potential
    # -----------------------------------------
    if total > 100000:
        insights.append(
            "💰 Large monthly spending detected — "
            "potential savings opportunity available"
        )

    # -----------------------------------------
    # Spending Stability
    # -----------------------------------------
    amounts = [
        float(e.amount)
        for e in expenses
    ]

    try:
        volatility = statistics.stdev(amounts)

        if volatility > avg:
            insights.append(
                "📈 Spending volatility is high"
            )
        else:
            insights.append(
                "📉 Spending pattern is relatively stable"
            )

    except Exception:
        pass

    return insights


# =========================================================
# 🤖 5. MASTER ANALYTICS ENGINE
# =========================================================
def generate_analytics_report(
    expenses,
    monthly_budget=30000
):

    total_spent = round(
        sum(float(e.amount) for e in expenses),
        2
    )

    return {
        "summary": {
            "total_transactions": len(expenses),
            "total_spent": total_spent
        },

        "monthly_trend": monthly_trend(expenses),

        "anomalies": detect_anomalies(expenses),

        "burn_rate": burn_rate(
            expenses,
            monthly_budget
        ),

        "insights": smart_insights(expenses)
    }