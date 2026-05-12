from datetime import datetime

ALLOWED_CATEGORIES = [
    "Food",
    "Transport",
    "Shopping",
    "Bills",
    "Rent",
    "Health",
    "Education",
    "Entertainment",
    "Others"
]


def normalize_category(category: str):
    if not category:
        return "Others"

    category = category.strip().title()

    if category not in ALLOWED_CATEGORIES:
        return "Others"

    return category


def clean_expense(data):
    return {
        "amount": float(data.get("amount", 0)),
        "category": normalize_category(data.get("category")),
        "date": data.get("date"),
        "month": data.get("date", "")[:7] if data.get("date") else "",
        "description": data.get("description", "")
    }