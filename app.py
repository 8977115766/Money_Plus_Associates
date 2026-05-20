
from flask import Flask, render_template, abort
import os

app = Flask(__name__)

LOAN_PRODUCTS = {
    "personal": {
        "title": "Premium Personal Loans",
        "icon": "fa-user-tie",
        "tagline": "Fast financing solutions",
        "interest_rate": "9.99%",
        "max_limit": "25 Lakhs",
        "max_tenure": "60 Months",
        "min_cibil": "650+",
        "age_limit": "21-58",
        "eligibility_notes": [
            "Indian Citizen",
            "Minimum 1 year experience"
        ],
        "documents": [
            "PAN Card",
            "Bank Statements"
        ]
    }
}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/loans")
def loans():
    return render_template("loans.html", products=LOAN_PRODUCTS)

@app.route("/loans/<category>")
def loan_detail(category):
    if category not in LOAN_PRODUCTS:
        abort(404)

    return render_template(
        "product_detail.html",
        product=LOAN_PRODUCTS[category]
    )

@app.route("/benefits")
def benefits():
    return render_template("benefits.html")

@app.route("/history")
def history():
    return render_template("history.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
