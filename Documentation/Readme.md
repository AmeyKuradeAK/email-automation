# Project Overview

## Email Automation
The Email Automation tool is a Python-based solution that simplifies the process of sending mass emails. It’s designed to read a list of email addresses from a CSV file and automatically send a customized message to each recipient. The email content is written in a Markdown (.md) file, giving you flexibility to format your message easily.

## Features
* **Bulk Email Sending:** Automatically emails all addresses in a provided CSV file, ideal for reaching large audiences.
* **Markdown Support:** Allows message content to be written in Markdown, giving you control over formatting and presentation.
* **Simple Authentication:** Uses an app-specific password for email server authentication, eliminating the need for complex login setups.

## System Requirements
* Python 3.x installed on your system
* Required libraries:
    * smtplib for SMTP operations
    * csv for reading email addresses
    * markdown for converting Markdown files to HTML format

You will also need SMTP server credentials, including an app-specific password for secure, straightforward authentication.

## Usage
1. **Prepare the CSV File:** Create a CSV file containing a column of email addresses.
2. **Write the Email Content:** Compose your email message in a Markdown (.md) file for flexible formatting.

## Core Libraries Used

The project leverages several key libraries:

* ```email.mime.text``` and ```email.mime.multipart```: To create versatile email messages in both plain text and HTML formats.
* ```smtplib```: Manages the SMTP connection and sends the emails.
* ```os```: Supports file management and path handling.
* ```markdown```: Converts Markdown content to HTML, enabling rich formatting in email messages.
* ```csv```: Reads and processes the CSV file with recipient email addresses.

Each library plays a specific role in streamlining and automating the email process.