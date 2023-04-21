import smtplib
import ssl
from email.message import EmailMessage
import os
import constants as const


def noise():
    '''Make noise after finishing executing a code'''
    duration = 1  # seconds
    freq = 440  # Hz
    os.system('play -nq -t alsa synth {} sine {}'.format(duration, freq))


def voice():
    for i in range(10):
        os.system('espeak "Ticket kaata hoyechee"')


def mail():
    # Define email sender and receiver
    email_sender = const.SENDER_EMAIL
    email_password = const.GMAIL_PASS
    email_receiver = [const.RECEIVER_EMAIL]

    # Set the subject and body of the email
    subject = 'Train Ticket Confirmed!!!'
    body = """
    Your train ticket is selected. Finish purchase within 15 minutes.
    """

    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(body)

    # Add SSL (layer of security)
    context = ssl.create_default_context()

    # Log in and send the email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())
