from flask import Flask, render_template, abort, request
import smtplib
from email.mime.text import MIMEText
import os

app = Flask(__name__)

# Loan Products Database
LOAN_PRODUCTS = {

    'personal': {
        'title': 'Premium Personal Loans',
        'icon': 'fa-user-tie',
        'tagline': 'Fast secured financing solutions.',
        'interest_rate': 'Starting at 9.99% p.a.'
    },

    'business': {
        'title': 'Strategic Business Capital',
        'icon': 'fa-chart-line',
        'tagline': 'Business expansion and working capital.',
        'interest_rate': 'Starting at 13.0% p.a.'
    },

    'educational': {
        'title': 'Global Educational Loans',
        'icon': 'fa-user-graduate',
        'tagline': 'Domestic and international education support.',
        'interest_rate': 'Starting at 8.75% p.a.'
    },

    'house': {
        'title': 'Premium Asset House Loans',
        'icon': 'fa-house-chimney',
        'tagline': 'Flexible home financing solutions.',
        'interest_rate': 'Starting at 8.40% p.a.'
    }
}


# HOME PAGE
@app.route('/')
def index():
    return render_template('index.html')


# LOANS PAGE
@app.route('/loans')
def loans():
    return render_template('loans.html', products=LOAN_PRODUCTS)


# LOAN DETAILS
@app.route('/loans/<category>')
def loan_detail(category):

    if category not in LOAN_PRODUCTS:
        abort(404)

    product_data = LOAN_PRODUCTS[category]

    return render_template(
        'product_detail.html',
        product=product_data
    )


# BENEFITS PAGE
@app.route('/benefits')
def benefits():
    return render_template('benefits.html')


# HISTORY PAGE
@app.route('/history')
def history():
    return render_template('history.html')


# LEAD FORM SUBMISSION
@app.route('/submit-lead', methods=['POST'])
def submit_lead():

    try:

        # FORM DATA
        name = request.form.get('name')
        phone = request.form.get('phone')

        # EMAIL SETTINGS
        sender_email = "dmemoneyplus@gmail.com"

        app_password = os.environ.get("EMAIL_PASSWORD")

        receiver_email = "dmemoneyplus@gmail.com"

        # CHECK PASSWORD
        if not app_password:
            return "EMAIL_PASSWORD environment variable not set"

        # EMAIL CONTENT
        subject = "New Loan Lead - Money Plus"

        body = f"""
New Customer Lead

Name: {name}

Phone: {phone}
"""

        # EMAIL MESSAGE
        msg = MIMEText(body)

        msg['Subject'] = subject
        msg['From'] = sender_email
        msg['To'] = receiver_email

        # SMTP CONNECTION
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)

        server.login(sender_email, app_password)

        server.send_message(msg)

        server.quit()

        return """
        <script>
        alert('Submitted Successfully!');
        window.location.href='/';
        </script>
        """

    except Exception as e:

        return f"""
        <h1>Email Error</h1>
        <pre>{str(e)}</pre>
        """


# RUN APP
if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))

    app.run(host="0.0.0.0", port=port)
