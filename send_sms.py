#!/usr/bin/env python3
"""
Consciousness Revolution - SMS Sender
Send SMS messages via email-to-SMS carrier gateways.

Usage:
    python send_sms.py <phone_number> <message> [carrier]

Carriers:
    verizon   - @vtext.com (default)
    tmobile   - @tmomail.net
    att       - @txt.att.net
    sprint    - @messaging.sprintpcs.com
    boost     - @sms.myboostmobile.com
    cricket   - @mms.cricketwireless.net

Examples:
    python send_sms.py 4065803779 "Hello Commander" verizon
    python send_sms.py 5094963855 "Hello ODB" verizon
    python send_sms.py 12674439742 "Hello Joshua" verizon

Quick Reference:
    Derek (COMMANDER): 4065803779
    Josh (ODB): 5094963855
    Joshua Serrano: 12674439742
"""

import smtplib
import sys
import os
from email.mime.text import MIMEText
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
FROM_EMAIL = os.getenv("EMAIL_FROM", "odb1original@gmail.com")
APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD", "")

# SMS Gateway map
SMS_GATEWAYS = {
    "verizon": "@vtext.com",
    "tmobile": "@tmomail.net",
    "att": "@txt.att.net",
    "sprint": "@messaging.sprintpcs.com",
    "boost": "@sms.myboostmobile.com",
    "cricket": "@mms.cricketwireless.net",
}

# Known team phone numbers with carriers
TEAM_PHONES = {
    "4065803779": {"name": "COMMANDER (Derek)", "carrier": "verizon"},
    "5094963855": {"name": "ODB (Josh)", "carrier": "verizon"},
    "12674439742": {"name": "Joshua Serrano", "carrier": "verizon"},
}


def clean_phone_number(phone: str) -> str:
    """Remove all non-digit characters from phone number."""
    return ''.join(filter(str.isdigit, phone))


def send_sms(phone: str, message: str, carrier: str = "verizon") -> bool:
    """
    Send an SMS via email-to-SMS gateway.

    Args:
        phone: Phone number (digits only, or will be cleaned)
        message: SMS message (will be truncated to 160 chars)
        carrier: Carrier name (verizon, tmobile, att, sprint, boost, cricket)

    Returns:
        True if sent successfully, False otherwise
    """
    if not APP_PASSWORD:
        print("ERROR: No Gmail App Password configured.")
        print("Set GMAIL_APP_PASSWORD in .env file")
        return False

    # Clean phone number
    phone = clean_phone_number(phone)

    # Get carrier gateway
    carrier_lower = carrier.lower()
    if carrier_lower not in SMS_GATEWAYS:
        print(f"ERROR: Unknown carrier '{carrier}'")
        print(f"Available carriers: {', '.join(SMS_GATEWAYS.keys())}")
        return False

    gateway = SMS_GATEWAYS[carrier_lower]
    to_address = f"{phone}{gateway}"

    # Truncate message for SMS
    if len(message) > 160:
        print(f"WARNING: Message truncated from {len(message)} to 160 characters")
        message = message[:157] + "..."

    # Create simple text message
    msg = MIMEText(message)
    msg['From'] = FROM_EMAIL
    msg['To'] = to_address
    msg['Subject'] = ""  # SMS doesn't use subject

    try:
        # Connect to Gmail SMTP
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(FROM_EMAIL, APP_PASSWORD)
            server.sendmail(FROM_EMAIL, to_address, msg.as_string())

        # Get recipient name if known
        recipient_name = TEAM_PHONES.get(phone, {}).get("name", phone)
        print(f"SUCCESS: SMS sent to {recipient_name}")
        print(f"Gateway: {to_address}")
        print(f"Message: {message}")
        return True

    except smtplib.SMTPAuthenticationError:
        print("ERROR: Gmail authentication failed.")
        print("Check your App Password and ensure 2FA is enabled on Gmail.")
        return False
    except Exception as e:
        print(f"ERROR: Failed to send SMS: {e}")
        return False


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)

    phone = sys.argv[1]
    message = sys.argv[2]
    carrier = sys.argv[3] if len(sys.argv) > 3 else "verizon"

    # Auto-detect carrier for known numbers
    clean_number = clean_phone_number(phone)
    if clean_number in TEAM_PHONES and len(sys.argv) < 4:
        carrier = TEAM_PHONES[clean_number]["carrier"]
        print(f"Auto-detected carrier for {TEAM_PHONES[clean_number]['name']}: {carrier}")

    success = send_sms(phone, message, carrier)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
