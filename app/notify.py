import os
import smtplib
from email.message import EmailMessage


EMAIL_ADDRESS = os.environ.get('EMAIL_USER')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASS')

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
#>>  sends an email to gmail account notifying listing match
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

def send_email(subject, message):

    msg = EmailMessage()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = EMAIL_ADDRESS
    msg['Subject'] = 'TradeMe Match - ' + subject
    msg.set_content(message)

    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.starttls()
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)