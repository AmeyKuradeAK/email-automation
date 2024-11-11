from email.mime.text import MIMEText 
from email.mime.multipart import MIMEMultipart 
import smtplib 
import os 
from markdown import Markdown 
import csv
from dotenv import load_dotenv  # Import the dotenv library

# Load environment variables from .env file
load_dotenv()

# Retrieve the Gmail app password from the .env file
GMAIL_APP_PASSWORD = os.getenv('GMAIL_APP_PASSWORD')

if not GMAIL_APP_PASSWORD:
    print("Error: GMAIL_APP_PASSWORD is not set in the .env file.")
    exit()

# initialize connection to our email server, we will use gmail here
smtp = smtplib.SMTP('smtp.gmail.com', 587) 
smtp.ehlo() 
smtp.starttls() 

# Login with your email and the app password from .env
smtp.login('ameykurade60@gmail.com', GMAIL_APP_PASSWORD) 

def convert_markdown_to_html(markdown_text):
    """
    Converts Markdown text to HTML using the Markdown library.
    """
    markdown_converter = Markdown()
    return markdown_converter.convert(markdown_text)

def message(subject, content): 
    """
    Creates an email message object.
    """
    msg = MIMEMultipart() 
    msg['Subject'] = subject 
    html_text = convert_markdown_to_html(content)
    msg.attach(MIMEText(html_text, 'html'))
    return msg 

# Set the path to the Markdown file directly
message_file_path = "./custom_message.md"

# Read the message content from the file
try:
    with open(message_file_path, 'r') as message_file:
        message_content = message_file.read()
except FileNotFoundError:
    print("Error: File not found. Please check the path and try again.")
    exit()

# Read recipient emails from the CSV file
csv_file_path = "./custom.csv"
recipients = []
try:
    with open(csv_file_path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            recipients.append(row[0])  # Assuming email addresses are in the first column (index 0)
except FileNotFoundError:
    print("Error: CSV file not found. Please try again.")
    exit()

# Create the message object
msg = message("Custom Email Notification", message_content)

# Send the email to each recipient
for recipient in recipients:
    try:
        smtp.sendmail(from_addr="3dblends@gmail.com", to_addrs=recipient, msg=msg.as_string())
    except Exception as e:
        print(f"Failed to send email to {recipient}: {e}")

# Close the connection
smtp.quit()
