from flask import Blueprint, request, jsonify
from models.expense import Expense
from extensions import db
from datetime import datetime

expense_bp = Blueprint("expense", __name__)

# =========================
# ➕ ADD EXPENSE (SAFE + VALIDATION)
# =========================
@expense_bp.route("/add", methods=["POST"])
def add_expense():
    data = request.get_json()

    try:
        if not data:
            return jsonify({"error": "No input data provided"}), 400

        amount = data.get("amount")
        category = data.get("category")
        date = data.get("date")
        description = data.get("description", "")

        # Validation
        if amount is None or category is None or date is None:
            return jsonify({"error": "Missing required fields"}), 400

        expense = Expense(
            amount=float(amount),
            category=str(category).lower().strip(),
            date=datetime.strptime(date, "%Y-%m-%d") if "-" in date else date,
            description=description
        )

        db.session.add(expense)
        db.session.commit()

        return jsonify({
            "message": "Expense added successfully",
            "data": {
                "amount": amount,
                "category": category,
                "date": str(date)
            }
        }), 201

    except Exception as e:
        return jsonify({
            "error": str(e),
            "message": "Failed to add expense"
        }), 400


# =========================
# 📊 GET ALL EXPENSES
# =========================
@expense_bp.route("/all", methods=["GET"])
def get_expenses():
    try:
        expenses = Expense.query.order_by(Expense.id.desc()).all()

        return jsonify([
            {
                "id": e.id,
                "amount": e.amount,
                "category": e.category,
                "date": str(e.date),
                "description": e.description
            }
            for e in expenses
        ])

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# =========================
# 🧹 CLEAR ALL EXPENSES
# =========================
@expense_bp.route("/clear", methods=["DELETE"])
def clear_expenses():
    try:
        db.session.query(Expense).delete()
        db.session.commit()

        return jsonify({
            "message": "All expenses cleared successfully"
        })

    except Exception as e:
        return jsonify({
            "error": str(e),
            "message": "Failed to clear expenses"
        }), 500