#!/usr/bin/env python3
"""
Consciousness Revolution - Email Sender
Send emails via Gmail SMTP with App Password authentication.

Usage:
    python send_email.py <to_email> <subject> <message> [app_password]

Examples:
    python send_email.py commander@100xbuilder.io "Test Subject" "Hello from ODB"
    python send_email.py commander@100xbuilder.io "Subject" "Message" porstbzdzpdpbide
"""

import smtplib
import sys
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
FROM_EMAIL = os.getenv("EMAIL_FROM", "odb1original@gmail.com")
FROM_NAME = os.getenv("EMAIL_NAME", "ODB")
DEFAULT_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD", "")


def send_email(to_email: str, subject: str, message: str, app_password: str = None) -> bool:
    """
    Send an email via Gmail SMTP.

    Args:
        to_email: Recipient email address
        subject: Email subject line
        message: Email body text
        app_password: Gmail App Password (optional, uses env if not provided)

    Returns:
        True if sent successfully, False otherwise
    """
    password = app_password or DEFAULT_APP_PASSWORD

    if not password:
        print("ERROR: No Gmail App Password provided.")
        print("Either pass it as argument or set GMAIL_APP_PASSWORD in .env")
        return False

    # Create message
    msg = MIMEMultipart()
    msg['From'] = f"{FROM_NAME} <{FROM_EMAIL}>"
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))

    try:
        # Connect to Gmail SMTP
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(FROM_EMAIL, password)
            server.sendmail(FROM_EMAIL, to_email, msg.as_string())

        print(f"SUCCESS: Email sent to {to_email}")
        print(f"Subject: {subject}")
        return True

    except smtplib.SMTPAuthenticationError:
        print("ERROR: Gmail authentication failed.")
        print("Check your App Password and ensure 2FA is enabled on Gmail.")
        return False
    except Exception as e:
        print(f"ERROR: Failed to send email: {e}")
        return False


def main():
    if len(sys.argv) < 4:
        print(__doc__)
        print("\nQuick Reference:")
        print("  Commander: commander@100xbuilder.io")
        print("  ODB: odb1original@gmail.com")
        print("  Joshua: joshua.serrano2022@gmail.com")
        sys.exit(1)

    to_email = sys.argv[1]
    subject = sys.argv[2]
    message = sys.argv[3]
    app_password = sys.argv[4] if len(sys.argv) > 4 else None

    success = send_email(to_email, subject, message, app_password)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
