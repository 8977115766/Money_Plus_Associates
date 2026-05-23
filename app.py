from flask import Flask, render_template, abort
import os
import urllib.parse  # Correct library to handle the message spacing

app = Flask(__name__)

# Structured database matching Indian NBFC guidelines
LOAN_PRODUCTS = {
    'personal': {
        'title': 'Personal Loans',
        'icon': 'fa-user-tie',
        'tagline': 'Fast, secured financing for your life milestones and immediate cash flows.',
        'min_salary': '₹35,000 / month (net)',
        'min_cibil': '675+',
        'age_limit': '20 - 61 Years',
        'interest_rate': 'Starting at 9.99% ',
        'max_tenure': 'Up to 72 Months',
        'max_limit': 'Up to ₹50 Lakhs',
        'processing_fee': '1.5% to 2.5% of loan amount',
        'eligibility_notes': [
            'Applicant must be an Indian Citizen with verified employment.',
            'Must be a salaried professional or registered service contractor.',
            'Salary must be regularly credited directly into a valid bank account.',
            'Minimum continuous work experience of 1 year with current employer.'
        ],
        'documents': [
            'PAN Card (Mandatory identity registration link)',
            'Identity/Address verification documentation (e.g., Aadhaar Card/Passport)',
            'Salary Slips for the last 3 months to verify income stability',
            'Bank account statement for the past 6 months showing salary credits'
        ]
    },
    'business': {
        'title': 'Business Loans',
        'icon': 'fa-chart-line',
        'tagline': 'Flexible funding solutions to support business growth, daily operations, and expansion plans.',
        'min_salary': '₹5 Lakhs Annual Turn-over',
        'min_cibil': '700+ (Commercial/Company Score)',
        'age_limit': '25 - 65 Years',
        'interest_rate': 'Starting at 10.5% ',
        'max_tenure': 'Up to 60 Months',
        'max_limit': 'No-Limit',
        'processing_fee': '2.0% Flat Admin Surcharge',
        'eligibility_notes': [
            'Business entity must have an active operational history of at least 3 years.',
            'Profitable trading sheets over the preceding two financial years.',
            'Enterprise registration status must conform to local regulatory norms.',
            'GST return profiles must be clean with no missing transaction filings.'
        ],
        'documents': [
            'PAN Cards of Proprietor/Partners/Directors alongside Company PAN',
            'GST Registration Certificate & filing declarations for the trailing 12 months',
            'Audited Financial Balance Sheets and P&L accounts for past 2 years',
            'Primary operational Bank Statements covering the past 12 months'
        ]
    },
    'educational': {
        'title': 'Educational Loans',
        'icon': 'fa-user-graduate',
        'tagline': 'Helping students achieve their academic dreams with easy and reliable education financing.',
        'min_salary': '₹25,000 / month (Co-borrower income)',
        'min_cibil': '650+ (Evaluated via Primary Co-borrower)',
        'age_limit': '18 - 30 Years (Student profile bracket)',
        'interest_rate': 'Starting at 11.99% ',
        'max_tenure': 'Up to 4 Years (Includes moratorium breaks)',
        'max_limit': 'As Per Norms',
        'processing_fee': 'Zero fee options available for premier domestic universities',
        'eligibility_notes': [
            'Student must have secured confirmed admission into a recognized course.',
            'A salaried or self-employed co-borrower (parent/guardian) is mandatory.',
            'Course profile must offer viable employment scope post-completion.',
            'Collateral documentation is required for international loan thresholds exceeding 7.5L.'
        ],
        'documents': [
            'Confirmed Admission Letter containing structural Fee Schedule breakdown',
            'Academic Marksheets & Certificates (10th, 12th, Graduation as applicable)',
            'KYC records & Income verification tracking metrics of the Co-borrower',
            'Collateral asset property deeds (Only required for high-tier unsecured overrides)'
        ]
    },
    'house': {
        'title': 'Home & Property Loans',
        'icon': 'fa-house-chimney',
        'tagline': 'Simple and secure financing options to help you invest in your dream home or property with confidence.',
        'min_salary': '₹35,000 / month (Combined household income)',
        'min_cibil': '680+',
        'age_limit': '21 - 65 Years',
        'interest_rate': 'Starting at 7.65% p.a. (Balanced Floating Base)',
        'max_tenure': 'Up to 30 Scalable Years',
        'max_limit': 'Up to 80% to 90% of Market Property Value Valuation',
        'processing_fee': '₹5,000 to 0.5% capped technical vetting fee',
        'eligibility_notes': [
            'Applicants can include co-applicants (spouse/parents) to enhance eligibility limits.',
            'Property under assessment must passess unencumbered legal titles.',
            'Construction project updates must fit structural safety approvals.',
            'Consistent income parameters with verifiable tax filing compliance.'
        ],
        'documents': [
            'Allotment Letter, Sale Agreement, or original Title Deeds history documentation',
            'No Objection Certificate (NOC) issued by builders or competent authorities',
            'Form 16 declarations alongside ITR files for the last 2 consecutive years',
            'Approved construction plan blueprints matched with technical validation stamps and Form 16'
            
        ]
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
    return render_template('product_detail.html', product=product_data)

@app.route('/benefits')
def benefits():
    return render_template('benefits.html')

@app.route('/history')
def history():
    return render_template('history.html')
@app.route('/contact')
def contact():
    return render_template('contact.html')


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
