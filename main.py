# Import the following module 
from email.mime.text import MIMEText 
from email.mime.image import MIMEImage 
from email.mime.application import MIMEApplication 
from email.mime.multipart import MIMEMultipart 
import smtplib 
import os 
from markdown import Markdown 

# initialize connection to our 
# email server, we will use gmail here 
smtp = smtplib.SMTP('smtp.gmail.com', 587) 
smtp.ehlo() 
smtp.starttls() 

# Login with your email and password 
smtp.login('ameykurade60@gmail.com', 'app-password') 

def read_message_from_file(filename):
  """
  Reads the contents of a Markdown file and returns them as a string.

  Args:
      filename (str): The path to the Markdown file.

  Returns:
      str: The contents of the Markdown file.
  """
  with open(filename, 'r') as file:
    return file.read()

# Function to convert Markdown to HTML
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

# send our email message 'msg' to our boss 
def message(subject="Python Notification", 
			img=None, 
			attachment=None,
            filename=None): 
	
    """
  Creates an email message object.

  Args:
      subject (str, optional): The email subject. Defaults to "Python Notification".
      filename (str, optional): The path to the Markdown file containing the message body.
          If not provided, the message body will be empty.
      img (str, optional): The path to the image attachment. Defaults to None.
      attachment (str, optional): The path to the attachment. Defaults to None.

  Returns:
      MIMEMultipart: The constructed email message object.
    """
 
	# build message contents 
    msg = MIMEMultipart() 
	
	# Add Subject 
    msg['Subject'] = subject 
    if filename:
        markdown_text = read_message_from_file(filename)
        html_text = convert_markdown_to_html(markdown_text)
        msg.attach(MIMEText(html_text, 'html'))  # Attach the converted HTML message
	
 
	# Add text contents 
	
    return msg 


# Call the message function 
msg = message("3D Blends", filename="custom_message.md")

# Make a list of emails, where you wanna send mail 
to = ["stecspport@gmail.com"] 

# Provide some data to the sendmail function! 
smtp.sendmail(from_addr="3dblends@gmail.com", 
			to_addrs=to, msg=msg.as_string()) 

# Finally, don't forget to close the connection 
smtp.quit()
