# ==========================================
# 🚨 ADVANCED ALERT SERVICE (FINAL VERSION)
# ==========================================

from datetime import datetime


# ==========================================
# 🧠 FINANCIAL HEALTH SCORE ENGINE
# ==========================================

def financial_health_score(spent, limit):

    try:
        spent = float(spent)
        limit = float(limit)

    except:
        return 0

    if limit <= 0:
        return 0

    usage = (spent / limit) * 100

    if usage <= 40:
        return 95

    elif usage <= 60:
        return 85

    elif usage <= 80:
        return 70

    elif usage <= 100:
        return 55

    elif usage <= 150:
        return 35

    return 15


# ==========================================
# 🎯 MAIN BUDGET ALERT ENGINE
# ==========================================

def budget_alert(spent, limit):

    try:
        spent = float(spent)
        limit = float(limit)

    except:
        return {
            "status": "ERROR",
            "message": "Invalid budget values",
            "color": "gray",
            "priority": 0,
            "generated_at": datetime.utcnow().isoformat()
        }

    # ==========================================
    # SAFETY CHECK
    # ==========================================

    if limit <= 0:

        return {
            "status": "INVALID",
            "message": "Budget limit must be greater than zero",
            "color": "gray",
            "priority": 0,
            "generated_at": datetime.utcnow().isoformat()
        }

    usage_percent = (spent / limit) * 100

    health_score = financial_health_score(
        spent,
        limit
    )

    # ==========================================
    # 🚨 ALERT LEVELS
    # ==========================================

    if usage_percent >= 300:

        return {
            "status": "EXTREME",
            "message": "💀 Extreme overspending detected",
            "usage_percent": round(usage_percent, 2),
            "overspent": round(spent - limit, 2),
            "health_score": health_score,
            "color": "darkred",
            "priority": 5,
            "generated_at": datetime.utcnow().isoformat()
        }

    elif usage_percent >= 150:

        return {
            "status": "CRITICAL",
            "message": "🚨 Critical budget overspending",
            "usage_percent": round(usage_percent, 2),
            "overspent": round(spent - limit, 2),
            "health_score": health_score,
            "color": "red",
            "priority": 4,
            "generated_at": datetime.utcnow().isoformat()
        }

    elif usage_percent >= 100:

        return {
            "status": "OVER_BUDGET",
            "message": "⚠️ Budget limit exceeded",
            "usage_percent": round(usage_percent, 2),
            "overspent": round(spent - limit, 2),
            "health_score": health_score,
            "color": "orange",
            "priority": 3,
            "generated_at": datetime.utcnow().isoformat()
        }

    elif usage_percent >= 80:

        return {
            "status": "WARNING",
            "message": "⚠️ 80% budget utilized",
            "usage_percent": round(usage_percent, 2),
            "remaining": round(limit - spent, 2),
            "health_score": health_score,
            "color": "gold",
            "priority": 2,
            "generated_at": datetime.utcnow().isoformat()
        }

    elif usage_percent >= 50:

        return {
            "status": "MODERATE",
            "message": "📊 Moderate spending level",
            "usage_percent": round(usage_percent, 2),
            "remaining": round(limit - spent, 2),
            "health_score": health_score,
            "color": "yellow",
            "priority": 1,
            "generated_at": datetime.utcnow().isoformat()
        }

    return {
        "status": "SAFE",
        "message": "✅ Financial spending is healthy",
        "usage_percent": round(usage_percent, 2),
        "remaining": round(limit - spent, 2),
        "health_score": health_score,
        "color": "green",
        "priority": 0,
        "generated_at": datetime.utcnow().isoformat()
    }


# ==========================================
# 🔥 DAILY SPENDING ALERT
# ==========================================

def daily_spending_alert(today_spending, limit):

    try:
        today_spending = float(today_spending)
        limit = float(limit)

    except:
        return {
            "status": "ERROR",
            "message": "Invalid spending values"
        }

    if limit <= 0:

        return {
            "status": "INVALID",
            "message": "Invalid budget limit"
        }

    daily_ratio = today_spending / limit

    if daily_ratio >= 0.50:

        return {
            "status": "EXTREME",
            "message": "💀 Massive daily spending spike detected"
        }

    elif daily_ratio >= 0.30:

        return {
            "status": "HIGH",
            "message": "🔥 High daily spending detected"
        }

    elif daily_ratio >= 0.15:

        return {
            "status": "MEDIUM",
            "message": "⚠️ Daily spending above normal"
        }

    return {
        "status": "NORMAL",
        "message": "✅ Daily spending looks healthy"
    }


# ==========================================
# 💎 SMART SAVING SUGGESTION
# ==========================================

def saving_suggestion(spent, limit):

    try:
        spent = float(spent)
        limit = float(limit)

    except:
        return {
            "status": "ERROR",
            "message": "Invalid savings data"
        }

    if limit <= 0:

        return {
            "status": "INVALID",
            "message": "Budget limit invalid"
        }

    remaining = limit - spent

    if remaining <= 0:

        return {
            "status": "NO_SAVINGS",
            "message": "❌ No savings remaining this month",
            "remaining": 0
        }

    save_percent = (remaining / limit) * 100

    if save_percent >= 40:

        return {
            "status": "EXCELLENT",
            "message": "💎 Excellent savings performance",
            "remaining": round(remaining, 2)
        }

    elif save_percent >= 20:

        return {
            "status": "GOOD",
            "message": "✅ Good savings balance maintained",
            "remaining": round(remaining, 2)
        }

    return {
        "status": "LOW",
        "message": "⚠️ Savings are getting low",
        "remaining": round(remaining, 2)
    }


# ==========================================
# 📅 MONTHLY SUMMARY ENGINE
# ==========================================

def monthly_summary(spent, limit):

    try:
        spent = float(spent)
        limit = float(limit)

    except:
        return {
            "status": "ERROR",
            "message": "Invalid monthly summary data"
        }

    if limit <= 0:

        return {
            "status": "INVALID",
            "message": "Budget limit invalid"
        }

    remaining = limit - spent

    alert = budget_alert(spent, limit)

    return {

        "month":
            datetime.now().strftime("%B %Y"),

        "spent":
            round(spent, 2),

        "budget":
            round(limit, 2),

        "remaining":
            round(max(remaining, 0), 2),

        "overspent":
            round(abs(remaining), 2)
            if remaining < 0 else 0,

        "usage_percent":
            round((spent / limit) * 100, 2),

        "health_score":
            financial_health_score(spent, limit),

        "status":
            alert["status"],

        "alert":
            alert["message"],

        "generated_at":
            datetime.utcnow().isoformat()
    }