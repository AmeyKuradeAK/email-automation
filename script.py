from email.mime.text import MIMEText 
from email.mime.multipart import MIMEMultipart 
import smtplib 
import os 
from markdown import Markdown 
import csv

# initialize connection to our 
# email server, we will use gmail here 
smtp = smtplib.SMTP('smtp.gmail.com', 587) 
smtp.ehlo() 
smtp.starttls() 

# Login with your email and password 
smtp.login('ameykurade60@gmail.com', 'lyflscxwvnnizfsk') 

def convert_markdown_to_html(markdown_text):
  """
  Converts Markdown text to HTML using the Markdown library.

  Args:
      markdown_text (str): The Markdown text to be converted.

  Returns:
      str: The converted HTML text.
  """
  markdown_converter = Markdown()
  return markdown_converter.convert(markdown_text)

# Function to create the email message 
def message(subject, content): 
  """
  Creates an email message object.

  Args:
      subject (str): The email subject.
      content (str): The email message body in Markdown format.

  Returns:
      MIMEMultipart: The constructed email message object.
  """
  
  msg = MIMEMultipart() 
  
  # Add Subject 
  msg['Subject'] = subject 
  
  # Convert Markdown content to HTML and attach
  html_text = convert_markdown_to_html(content)
  msg.attach(MIMEText(html_text, 'html'))
  
  return msg 

# Get the path to the Markdown file from the user
message_file = input("Enter the path to your Markdown message file: \n")

# Read the message content from the file
try:
  with open(message_file, 'r') as message_file:
    message_content = message_file.read()
except FileNotFoundError:
  print("Error: File not found. Please try again.")
  exit()

# Call the message function to create the message object
msg = message("3D Blends", message_content)

# Get the path to the CSV file with recipient emails
csv_file = input("Enter the path to your CSV file containing recipient emails: \n")

# Read recipient emails from the CSV file
recipients = []
try:
  with open(csv_file, 'r') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
      recipients.append(row[0])  # Assuming email addresses are in the first column (index 0)
except FileNotFoundError:
  print("Error: CSV file not found. Please try again.")
  exit()

# Call the message function to create the message object
msg = message("Custom Email Notification", message_content)

# Send the email to each recipient
for recipient in recipients:
  # Provide data to the sendmail function! 
  smtp.sendmail(from_addr="3dblends@gmail.com", 
                to_addrs=recipient, msg=msg.as_string())

# Finally, don't forget to close the connection 
smtp.quit()

