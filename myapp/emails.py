import logging
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import BadHeaderError
import smtplib

# Get the logger for your app
logger = logging.getLogger('myapp')  # Replace 'myapp' with the actual name of your app

def send_welcome_email(name, email):
    subject = "Welcome to Our Platform"
    plain_message = f"Hi {name},\n\nThank you for registering with us!"
    html_message = f"""
    <html>
    <body>
        <h1 style="color: blue;">Welcome, {name}!</h1>
        <p>Thank you for joining our platform. We are excited to have you here.</p>
        <p><a href="http://127.0.0.1:8000/sign_up/" style="color: green;">Click here to complete your sign-up</a></p>
    </body>
    </html>
    """
    
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [email]

    try:
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=from_email,
            recipient_list=recipient_list,
            html_message=html_message
        )
        logger.info(f"Welcome email sent to {email}")
    except BadHeaderError:
        logger.error(f"Invalid header found when sending email to {email}")
    except smtplib.SMTPException as smtp_error:
        logger.error(f"SMTP error occurred while sending email to {email}: {smtp_error}")
    except Exception as e:
        logger.error(f"Failed to send email to {email}: {e}")
        raise RuntimeError("Email sending failed")
