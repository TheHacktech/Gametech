import logging
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.mime.text import MIMEText
from config import GMAIL_USER, GMAIL_PASSWORD
from flask import escape

# Send an email to the designated email with the passed subject and html body
def send_email(email, subject, html, app_log=None):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = "Hacktech <" + GMAIL_USER + ">"
    msg['To'] = email
    msg.attach(MIMEText(html, 'html'))

    try:  
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(GMAIL_USER, GMAIL_PASSWORD)
        server.sendmail(GMAIL_USER, [email], msg.as_string())
        server.close()
        # logging.info('Sent Application Confirmation Email to %s', email)
        # print 'It worked!'
    except Exception, e:
        app_log.info('FAILED Sending Application Confirmation to %s', escape(email))
        # print 'Something went wrong...'
        # print str(e)

