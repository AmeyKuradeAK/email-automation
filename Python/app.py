from flask import Flask, request, jsonify
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import os
from markdown import Markdown
import csv
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Initialize SMTP connection
smtp = smtplib.SMTP('smtp.gmail.com', 587)
smtp.ehlo()
smtp.starttls()
smtp.login('ameykurade60@gmail.com', 'app-password')  # replace with your app password




# Markdown to HTML converter
def convert_markdown_to_html(markdown_text):
    markdown_converter = Markdown()
    return markdown_converter.convert(markdown_text)

# Create the email message object
def create_message(subject, content):
    msg = MIMEMultipart()
    msg['Subject'] = subject
    html_text = convert_markdown_to_html(content)
    msg.attach(MIMEText(html_text, 'html'))
    return msg

# Endpoint to send emails
@app.route('/send-emails', methods=['POST'])
def send_emails():
    subject = request.form.get('subject')
    markdown_file = request.files.get('markdown_file')
    csv_file = request.files.get('csv_file')

    if not all([subject, markdown_file, csv_file]):
        return jsonify({"error": "Missing subject, markdown file, or CSV file"}), 400

    # Read Markdown message content
    markdown_file_path = secure_filename(markdown_file.filename)
    markdown_file.save(markdown_file_path)
    with open(markdown_file_path, 'r') as f:
        message_content = f.read()

    # Read recipient emails from the CSV file
    csv_file_path = secure_filename(csv_file.filename)
    csv_file.save(csv_file_path)
    recipients = []
    try:
        with open(csv_file_path, 'r') as f:
            reader = csv.reader(f)
            recipients = [row[0] for row in reader]
    except Exception as e:
        return jsonify({"error": f"Error reading CSV file: {str(e)}"}), 500

    # Create email message object
    msg = create_message(subject, message_content)

    # Send email to each recipient
    for recipient in recipients:
        try:
            smtp.sendmail(from_addr="3dblends@gmail.com", to_addrs=recipient, msg=msg.as_string())
        except Exception as e:
            return jsonify({"error": f"Failed to send email to {recipient}: {str(e)}"}), 500

    return jsonify({"message": "Emails sent successfully"}), 200

# Close SMTP on app shutdown
@app.teardown_appcontext
def close_smtp_connection(exception=None):
    smtp.quit()

if __name__ == '__main__':
    app.run(port=5000)
