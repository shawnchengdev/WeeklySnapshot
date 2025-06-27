import smtplib
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from typing import Optional
import os

# Sends an email with optional file attachments
def email_files(sender_email: str, receiver_email: str, password: str, subject: str, body: str, files: Optional[list[str]]):
    print("\nPackaging email...")

    # Creates the email
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = Header(subject, "utf-8")
    msg.attach(MIMEText(body, "plain", "utf-8"))

    # Attaches each file to the email
    if files:
        for file_location in files:
            attachment = open(file_location, "rb") # Reads the file in binary

            attachment_package = MIMEBase("application", "octet-stream")
            attachment_package.set_payload(attachment.read())
            encoders.encode_base64(attachment_package)
            attachment_package.add_header("Content-Disposition", "attachment", filename=os.path.basename(file_location))
            msg.attach(attachment_package)

    # Tries sending the email through Gmail, the finally logic is implemented because the server will not automatically quit even when a error occurs
    try:
        server = smtplib.SMTP(host="smtp.gmail.com", port=587)
        print("Connecting to server...")
        server.starttls()
        server.login(sender_email, password)
        print("Sending email...")
        server.sendmail(msg["From"], receiver_email, msg.as_string())
        print("Sent email")
    except Exception:
        print("Email failed to send.")
    finally:
        server.quit()
