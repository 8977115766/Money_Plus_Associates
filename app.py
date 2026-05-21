@app.route('/submit-lead', methods=['POST'])
def submit_lead():

    try:

        name = request.form.get('name')
        phone = request.form.get('phone')

        sender_email = "dmemoneyplus@gmail.com"

        app_password = os.environ.get("EMAIL_PASSWORD")

        receiver_email = "dmemoneyplus@gmail.com"

        subject = "New Loan Lead - Money Plus"

        body = f"""
New Customer Lead

Name: {name}

Phone: {phone}
"""

        msg = MIMEText(body)

        msg['Subject'] = subject
        msg['From'] = sender_email
        msg['To'] = receiver_email

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
