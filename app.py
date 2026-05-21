from flask import Flask, render_template, abort
import os

app = Flask(__name__)

# Structured database matching Indian NBFC guidelines
LOAN_PRODUCTS = {
    'personal': {
        'title': 'Premium Personal Loans',
        'icon': 'fa-user-tie',
        'tagline': 'Fast, secured financing for your life milestones and immediate cash flows.',
        'min_salary': '₹35,000 / month (net)',
        'min_cibil': '650+',
        'age_limit': '21 - 58 Years',
        'interest_rate': 'Starting at 9.99% p.a.',
        'max_tenure': 'Up to 60 Months',
        'max_limit': 'Up to ₹25 Lakhs',
    },

    'business': {
        'title': 'Strategic Business Capital',
        'icon': 'fa-chart-line',
        'tagline': 'Fuel operational scale, equipment purchase, or short-term working capital demands.',
        'min_salary': '₹5 Lakhs Annual Turn-over',
        'min_cibil': '700+',
        'age_limit': '25 - 65 Years',
        'interest_rate': 'Starting at 13.0% p.a.',
        'max_tenure': 'Up to 48 Months',
        'max_limit': 'Up to ₹50 Lakhs',
    },

    'educational': {
        'title': 'Global Educational Loans',
        'icon': 'fa-user-graduate',
        'tagline': 'Funding academic futures across premier domestic and global institutions.',
        'min_salary': '₹25,000 / month (Co-borrower income)',
        'min_cibil': '620+',
        'age_limit': '18 - 35 Years',
        'interest_rate': 'Starting at 8.75% p.a.',
        'max_tenure': 'Up to 15 Years',
        'max_limit': 'Domestic: 20L | International: Up to ₹1.5 Cr',
    },

    'house': {
        'title': 'Premium Asset House Loans',
        'icon': 'fa-house-chimney',
        'tagline': 'Seamless long-horizon asset financing options.',
        'min_salary': '₹35,000 / month',
        'min_cibil': '680+',
        'age_limit': '21 - 65 Years',
        'interest_rate': 'Starting at 8.40% p.a.',
        'max_tenure': 'Up to 30 Years',
        'max_limit': 'Up to 90% Property Value',
    }
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/loans')
def loans():
    return render_template('loans.html', products=LOAN_PRODUCTS)

@app.route('/loans/<category>')
def loan_detail(category):
    if category not in LOAN_PRODUCTS:
        abort(404)

    product_data = LOAN_PRODUCTS[category]

    return render_template(
        'product_detail.html',
        product=product_data
    )

@app.route('/benefits')
def benefits():
    return render_template('benefits.html')

@app.route('/history')
def history():
    return render_template('history.html')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
