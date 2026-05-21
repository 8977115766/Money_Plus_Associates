from flask import Flask, render_template, abort, request, redirect, url_for, flash
import smtplib
from email.mime.text import MIMEText
import os

app = Flask(__name__)
# Added a secret key to support secure flash messaging/sessions if needed later
app.secret_key = os.environ.get("SECRET_KEY", "money_plus_fallback_secret_key")

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
        'processing_fee': '1.5% to 2.5% of loan amount',
        'eligibility_notes': [
            'Applicant must be an Indian Citizen with verified employment.',
            'Must be a salaried professional or registered service contractor.',
            'Salary must be regularly credited directly into a valid bank account.',
            'Minimum continuous work experience of 1 year with current employer.'
        ],
        'documents': [
            'PAN Card (Mandatory identity registration link)',
            'Identity/Address verification documentation (e.g., Passport)',
            'Salary Slips for the last 3 months to verify income stability',
            'Bank account statement for the past 6 months showing salary credits'
        ]
    },
    'business': {
        'title': 'Strategic Business Capital',
        'icon': 'fa-chart-line',
        'tagline': 'Fuel operational scale, equipment purchase, or short-term working capital demands.',
        'min_salary': '₹5 Lakhs Annual Turn-over',
        'min_cibil': '700+ (Commercial/Company Score)',
        'age_limit': '25 - 65 Years',
        'interest_rate': 'Starting at 13.0% p.a.',
        'max_tenure': 'Up to 48 Months',
        'max_limit': 'Up to ₹50 Lakhs (secured Collateral-Free)',
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
        'title': 'Global Educational Loans',
        'icon': 'fa-user-graduate',
        'tagline': 'Funding academic futures across premier domestic and global institutions.',
        'min_salary': '₹25,000 / month (Co-borrower income)',
        'min_cibil': '620+ (Evaluated via Primary Co-borrower)',
        'age_limit': '18 - 35 Years (Student profile bracket)',
        'interest_rate': 'Starting at 8.75% p.a.',
        'max_tenure': 'Up to 15 Years (Includes moratorium breaks)',
        'max_limit': 'Domestic: 20L | International: Up to ₹1.5 Cr',
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
        'title': 'Premium Asset House Loans',
        'icon': 'fa-house-chimney',
        'tagline': 'Seamless long-horizon asset financing options protecting your property investment.',
        'min_salary': '₹35,000 / month (Combined household income)',
        'min_cibil': '680+',
        'age_limit': '21 - 65 Years',
        'interest_rate': 'Starting at 8.40% p.a. (Balanced Floating Base)',
        'max_tenure': 'Up to 30 Scalable Years',
        'max_limit': 'Up to 80% to 90% of Market Property Value Valuation',
        'processing_fee': '₹5,000 to 0.5% capped technical vetting fee',
        'eligibility_notes': [
            'Applicants can include co-applicants (spouse/parents) to enhance eligibility limits.',
            'Property under assessment must possess unencumbered legal titles.',
            'Construction project updates must fit structural safety approvals.',
            'Consistent income parameters with verifiable tax filing compliance.'
        ],
        'documents': [
            'Allotment Letter, Sale Agreement, or original Title Deeds history documentation',
            'No Objection Certificate (NOC) issued by builders or competent authorities',
            'Form 16 declarations alongside ITR files for the last 2 consecutive years',
            'Approved construction plan blueprints matched with technical validation stamps'
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

@app.route('/submit-lead', methods=['POST'])
def submit_lead():
    try:
        # FORM DATA
        name = request.form.get('name')
        phone = request.form.get('phone')

        print(f"Form submission received - Name: {name}, Phone: {phone}")

        # EMAIL CONFIG
        sender_email = "dmemoneyplus@gmail.com"
        receiver_email = "dmemoneyplus@gmail.com"
        app_password = os.environ.get("EMAIL_PASSWORD")

        # CHECK ENV VARIABLE
        if not app_password:
            return "<h1>Configuration Error</h1><p>EMAIL_PASSWORD environment variable missing in Render dashboard.</p>", 500

        # EMAIL CONTENT
        subject = "New Loan Lead - Money Plus"
        body = f"New Customer Lead\n\nName: {name}\nPhone: {phone}"

        # MIME MESSAGE
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = sender_email
        msg['To'] = receiver_email

        # CLOUD-OPTIMIZED SMTP ROUTING (Using TLS over Port 587)
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()  # Upgrades the connection to secure TLS
        server.ehlo()
        server.login(sender_email, app_password)
        server.send_message(msg)
        server.quit()

        # Success handling via clean script injector
        return """
        <script>
            alert('Lead Submitted Successfully!');
            window.location.href = '/';
        </script>
        """

    except Exception as e:
        # This will now display the exact error on your screen if anything else fails
        return f"""
        <h1>Email Delivery System Error</h1>
        <p>Something went wrong while executing SMTP routing.</p>
        <pre>{str(e)}</pre>
        """, 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
