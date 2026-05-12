from flask import Blueprint, request, jsonify
from models.budget import Budget
from extensions import db

budget_bp = Blueprint("budget", __name__)

@budget_bp.route("/set", methods=["POST"])
def set_budget():
    data = request.json

    budget = Budget(
        category=data["category"],
        limit=data["limit"]
    )

    db.session.add(budget)
    db.session.commit()

    return jsonify({"message": "Budget saved"})


@budget_bp.route("/all", methods=["GET"])
def get_budget():
    budgets = Budget.query.all()

    return jsonify([
        {"category": b.category, "limit": b.limit}
        for b in budgets
    ])