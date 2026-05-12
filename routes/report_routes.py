from flask import Blueprint, send_file
from models.expense import Expense
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import datetime
import os

report_bp = Blueprint("report", __name__)

@report_bp.route("/download", methods=["GET"])
def download_report():

    expenses = Expense.query.all()

    filename = "fintrack_report.pdf"

    c = canvas.Canvas(filename, pagesize=letter)

    c.setFont("Helvetica-Bold", 16)
    c.drawString(180, 750, "FinTrack AI - Expense Report")

    c.setFont("Helvetica", 11)

    y = 700
    total = 0

    for e in expenses:
        line = f"{e.date} | {e.category} | ₹{e.amount}"
        c.drawString(50, y, line)
        y -= 20
        total += float(e.amount)

        if y < 60:
            c.showPage()
            y = 750

    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y - 20, f"Total Spent: ₹{total}")

    c.setFont("Helvetica", 10)
    c.drawString(50, 40, f"Generated: {datetime.datetime.now()}")

    c.save()

    return send_file(filename, as_attachment=True)